#!/usr/bin/env python3
"""Verify documentation identifiers against source code truth index.

Parses all Python source at ../ollim-bot/src/ollim_bot/ using ast to build a
truth index of every identifier. Parses each MDX page to extract inline
backtick-quoted terms (skipping code blocks). Cross-references and reports
mismatches.

Usage:
    uv run python verify_docs.py              # full scan
    uv run python verify_docs.py --page X.mdx # single page
    uv run python verify_docs.py --verbose     # per-identifier detail
    uv run python verify_docs.py --dump-index  # dump truth index as JSON
"""

import ast
import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

DOCS_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = DOCS_ROOT.parent / "ollim-bot"
SOURCE_DIR = SOURCE_ROOT / "src" / "ollim_bot"

# ---------------------------------------------------------------------------
# Allowlist — terms in backticks that are NOT source identifiers
# ---------------------------------------------------------------------------

ALLOWLIST: set[str] = {
    # Mintlify/MDX component names
    "Tabs", "Tab", "Steps", "Step", "Card", "Columns",
    "AccordionGroup", "Accordion", "Note", "Tip", "Warning", "Info",
    # Python/YAML builtins and type names
    "true", "false", "null", "None", "str", "int", "bool", "list",
    "dict", "float", "object", "type", "tuple", "set",
    # Python stdlib classes and builtins referenced in docs
    "ValueError", "TypeError", "KeyError", "ContextVar", "AsyncGenerator",
    "NamedTuple", "TypedDict", "YourName",
    "print",
    # Python stdlib modules
    "argparse", "atexit", "contextvars", "asyncio", "dataclasses",
    # discord.py classes and methods
    "DynamicItem", "application_info", "on_message", "on_ready",
    "message_content",
    # claude-agent-sdk classes and type aliases
    "ClaudeSDKClient", "ResultMessage", "StreamEvent", "AgentDefinition",
    "ClaudeAgentOptions", "Task", "AssistantMessage", "TextBlock",
    "SystemMessage", "HookMatcher", "SessionEventType", "ModelName",
    # APScheduler classes
    "AsyncIOScheduler", "DateTrigger", "CronTrigger",
    # google-auth / external library classes
    "InstalledAppFlow", "WebSearch", "WebFetch", "Authorization",
    # External functions / import aliases
    "load_dotenv", "application_info", "reset_permissions",
    # JSON Schema type names
    "string", "integer", "boolean", "number", "array",
    # Package/library names
    "uv", "git", "pip", "python", "bash", "npm", "pytest", "ruff",
    "discord.py", "APScheduler", "discord", "aiohttp", "jsonschema",
    "pyyaml", "apscheduler", "claude_agent_sdk",
    "ollim-bot",
    # File extensions
    ".md", ".mdx", ".json", ".jsonl", ".yaml", ".env", ".py", ".txt",
    ".toml",
    # YAML frontmatter delimiters that leak through
    "---",
    # Common doc patterns
    "Content coming soon.",
}

# Very common snake_case words that appear in backticks as prose, not as
# references to specific source identifiers. We skip these to avoid noise.
_COMMON_WORDS: set[str] = {
    "id", "name", "value", "type", "data", "key", "text", "status",
    "error", "result", "message", "title", "description", "action",
    "event", "query", "body", "path", "user", "channel", "token",
    "port", "host", "url", "slug", "summary", "content", "label",
    "style", "color", "fields", "format", "inline", "size",
    # Slash command parameter names / generic prose
    "default", "topic", "mode", "enabled", "instructions", "prompt",
    "critical", "resume", "capacity",
    # Programming terms used generically in prose
    "async", "args", "tools", "allowed", "denied", "cancelled", "prev",
    "dev", "bg", "fork", "enum", "utils", "helpers", "common",
    "on", "off", "editor", "stale", "msg_start",
    # JSON field names that are too generic to verify
    "message_id", "fork_session_id", "parent_session_id", "ts",
    "compact_boundary", "pre_tokens", "session_id",
    "custom_id",
    # Source module names referenced as prose (not Python identifiers)
    "agent_tools", "views",
    # Pytest fixture names and test terms
    "data_dir", "tmp_path",
    # Internal identifiers referenced by import alias or prose
    "agent_server", "max_thinking_tokens",
    "slash_fork", "check_fork_timeout",
    # SDK stream event type names (from claude-agent-sdk, not our source)
    "content_block_delta", "content_block_start", "content_block_stop",
    "input_json_delta", "tool_use",
    # MCP tool parameter names (JSON schema properties, not Python identifiers)
    "minutes_from_now", "refill_rate",
}


# ---------------------------------------------------------------------------
# Truth Index
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SourceIdentifier:
    name: str
    category: str
    source_file: str
    line: int


@dataclass
class TruthIndex:
    identifiers: dict[str, list[SourceIdentifier]] = field(default_factory=dict)

    def add(self, ident: SourceIdentifier) -> None:
        self.identifiers.setdefault(ident.name, []).append(ident)

    def contains(self, name: str) -> bool:
        return name in self.identifiers


# ---------------------------------------------------------------------------
# AST Extractors
# ---------------------------------------------------------------------------

def _rel_path(py_file: Path) -> str:
    return str(py_file.relative_to(SOURCE_ROOT))


def _extract_env_vars(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract os.environ["NAME"] and os.environ.get("NAME") patterns."""
    results: list[SourceIdentifier] = []
    for node in ast.walk(tree):
        # os.environ["NAME"]
        if isinstance(node, ast.Subscript):
            if (isinstance(node.value, ast.Attribute)
                    and isinstance(node.value.value, ast.Name)
                    and node.value.value.id == "os"
                    and node.value.attr == "environ"
                    and isinstance(node.slice, ast.Constant)
                    and isinstance(node.slice.value, str)):
                results.append(SourceIdentifier(
                    name=node.slice.value,
                    category="env_var",
                    source_file=path,
                    line=node.lineno,
                ))
        # os.environ.get("NAME") or os.environ.get("NAME", default)
        if isinstance(node, ast.Call):
            func = node.func
            if (isinstance(func, ast.Attribute)
                    and func.attr == "get"
                    and isinstance(func.value, ast.Attribute)
                    and isinstance(func.value.value, ast.Name)
                    and func.value.value.id == "os"
                    and func.value.attr == "environ"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)):
                results.append(SourceIdentifier(
                    name=node.args[0].value,
                    category="env_var",
                    source_file=path,
                    line=node.lineno,
                ))
    return results


def _extract_constants(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract module-level SCREAMING_CASE assignments."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        names: list[str] = []
        lineno = getattr(node, "lineno", 0)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.append(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.append(node.target.id)
        for name in names:
            if re.match(r"^_?[A-Z][A-Z0-9_]+$", name):
                results.append(SourceIdentifier(
                    name=name,
                    category="constant",
                    source_file=path,
                    line=lineno,
                ))
    return results


def _extract_classes(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract all class definitions at module level."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            results.append(SourceIdentifier(
                name=node.name,
                category="class",
                source_file=path,
                line=node.lineno,
            ))
    return results


def _is_dataclass(node: ast.ClassDef) -> bool:
    """Check if a class has @dataclass decorator."""
    for dec in node.decorator_list:
        if isinstance(dec, ast.Name) and dec.id == "dataclass":
            return True
        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Name) and dec.func.id == "dataclass":
            return True
    return False


def _extract_dataclass_fields(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract field names from @dataclass-decorated classes."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and _is_dataclass(node):
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    results.append(SourceIdentifier(
                        name=item.target.id,
                        category="dataclass_field",
                        source_file=path,
                        line=item.lineno,
                    ))
    return results


def _extract_functions(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract module-level function definitions."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results.append(SourceIdentifier(
                name=node.name,
                category="function",
                source_file=path,
                line=node.lineno,
            ))
    return results


def _extract_class_methods(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract method names from classes (e.g., Agent.stream_chat)."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if item.name.startswith("__") and item.name.endswith("__"):
                    continue  # skip dunder methods
                results.append(SourceIdentifier(
                    name=item.name,
                    category="method",
                    source_file=path,
                    line=item.lineno,
                ))
    return results


def _extract_typed_dict_fields(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract field names from TypedDict and NamedTuple classes."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        is_typed = any(
            (isinstance(base, ast.Name) and base.id in ("TypedDict", "NamedTuple"))
            or (isinstance(base, ast.Attribute) and base.attr in ("TypedDict", "NamedTuple"))
            for base in node.bases
        )
        if not is_typed:
            continue
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                results.append(SourceIdentifier(
                    name=item.target.id,
                    category="typed_dict_field",
                    source_file=path,
                    line=item.lineno,
                ))
    return results


def _extract_handler_dict_keys(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract string keys from handler dispatch dicts (e.g., button action handlers)."""
    results: list[SourceIdentifier] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        # Only extract from dicts where all keys are short lowercase strings
        # and all values are names (function references) — handler pattern
        if not node.keys or len(node.keys) < 3:
            continue
        all_str_keys = all(
            isinstance(k, ast.Constant) and isinstance(k.value, str)
            for k in node.keys if k is not None
        )
        all_name_values = all(
            isinstance(v, ast.Name) for v in node.values
        )
        if all_str_keys and all_name_values:
            for k in node.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    results.append(SourceIdentifier(
                        name=k.value,
                        category="handler_key",
                        source_file=path,
                        line=k.lineno,
                    ))
    return results


def _extract_mcp_tools(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract @tool("name", ...) decorator first-arg strings."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if (isinstance(dec, ast.Call)
                    and isinstance(dec.func, ast.Name)
                    and dec.func.id == "tool"
                    and dec.args
                    and isinstance(dec.args[0], ast.Constant)
                    and isinstance(dec.args[0].value, str)):
                results.append(SourceIdentifier(
                    name=dec.args[0].value,
                    category="mcp_tool",
                    source_file=path,
                    line=node.lineno,
                ))
    return results


def _extract_slash_commands(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract @bot.tree.command(name="...") patterns."""
    results: list[SourceIdentifier] = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call):
                continue
            func = dec.func
            # Match bot.tree.command(name="...")
            if (isinstance(func, ast.Attribute)
                    and func.attr == "command"
                    and isinstance(func.value, ast.Attribute)
                    and func.value.attr == "tree"):
                for kw in dec.keywords:
                    if (kw.arg == "name"
                            and isinstance(kw.value, ast.Constant)
                            and isinstance(kw.value.value, str)):
                        cmd_name = kw.value.value
                        results.append(SourceIdentifier(
                            name=f"/{cmd_name}",
                            category="slash_command",
                            source_file=path,
                            line=node.lineno,
                        ))
    return results


def _extract_cli_commands(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract argparse subcommand names and flags."""
    results: list[SourceIdentifier] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        # sub.add_parser("name") — CLI subcommands
        if (isinstance(func, ast.Attribute)
                and func.attr == "add_parser"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            results.append(SourceIdentifier(
                name=node.args[0].value,
                category="cli_subcommand",
                source_file=path,
                line=node.lineno,
            ))
        # add_argument("--flag") — CLI flags
        if (isinstance(func, ast.Attribute)
                and func.attr == "add_argument"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            flag = node.args[0].value
            if flag.startswith("-"):
                results.append(SourceIdentifier(
                    name=flag,
                    category="cli_flag",
                    source_file=path,
                    line=node.lineno,
                ))
            # Also capture short alias if present
            if (len(node.args) >= 2
                    and isinstance(node.args[1], ast.Constant)
                    and isinstance(node.args[1].value, str)
                    and node.args[1].value.startswith("-")):
                results.append(SourceIdentifier(
                    name=node.args[1].value,
                    category="cli_flag",
                    source_file=path,
                    line=node.lineno,
                ))
    return results


def _extract_cli_routes(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract CLI route names from the routes dict in main.py."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Dict):
                for key in child.keys:
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        val = key.value
                        if val in ("routine", "reminder", "tasks", "cal", "gmail"):
                            results.append(SourceIdentifier(
                                name=val,
                                category="cli_subcommand",
                                source_file=path,
                                line=key.lineno,
                            ))
    return results


def _extract_literal_types(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract string values from Literal[...] type aliases (e.g., SessionEventType)."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        # TypeAlias = Literal["a", "b", "c"]
        target_name = None
        value = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            if isinstance(node.targets[0], ast.Name):
                target_name = node.targets[0].id
                value = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_name = node.target.id
            value = node.value
        if value is None:
            continue
        # Check for Literal[...] subscript
        if (isinstance(value, ast.Subscript)
                and isinstance(value.value, ast.Name)
                and value.value.id == "Literal"):
            slice_node = value.slice
            elements: list[ast.expr] = []
            if isinstance(slice_node, ast.Tuple):
                elements = slice_node.elts
            else:
                elements = [slice_node]
            for elt in elements:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    results.append(SourceIdentifier(
                        name=elt.value,
                        category="literal_type_value",
                        source_file=path,
                        line=elt.lineno,
                    ))
    return results


def _extract_enum_members(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract Enum member names and values."""
    results: list[SourceIdentifier] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        is_enum = any(
            (isinstance(base, ast.Name) and base.id == "Enum")
            or (isinstance(base, ast.Attribute) and base.attr == "Enum")
            for base in node.bases
        )
        if not is_enum:
            continue
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        # Member name (e.g., SAVE)
                        results.append(SourceIdentifier(
                            name=target.id,
                            category="enum_member",
                            source_file=path,
                            line=item.lineno,
                        ))
                        # Member value (e.g., "save")
                        if isinstance(item.value, ast.Constant) and isinstance(item.value.value, str):
                            results.append(SourceIdentifier(
                                name=item.value.value,
                                category="enum_value",
                                source_file=path,
                                line=item.lineno,
                            ))
    return results


def _extract_choices_values(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract string values from argparse choices= and discord.app_commands.Choice patterns."""
    results: list[SourceIdentifier] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.keyword):
            continue
        # choices=["always", "on_ping", ...] in argparse
        if node.arg == "choices" and isinstance(node.value, ast.List):
            for elt in node.value.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    results.append(SourceIdentifier(
                        name=elt.value,
                        category="choice_value",
                        source_file=path,
                        line=elt.lineno,
                    ))
        # app_commands.Choice(name="x", value="x")
        if node.arg == "name" and isinstance(node.value, ast.List):
            for elt in node.value.elts:
                if isinstance(elt, ast.Call):
                    for kw in elt.keywords:
                        if (kw.arg == "value"
                                and isinstance(kw.value, ast.Constant)
                                and isinstance(kw.value.value, str)):
                            results.append(SourceIdentifier(
                                name=kw.value.value,
                                category="choice_value",
                                source_file=path,
                                line=kw.value.lineno,
                            ))
    return results


def _extract_contextvar_names(tree: ast.Module, path: str) -> list[SourceIdentifier]:
    """Extract ContextVar("name") string names."""
    results: list[SourceIdentifier] = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "ContextVar"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)):
            results.append(SourceIdentifier(
                name=node.args[0].value,
                category="contextvar",
                source_file=path,
                line=node.lineno,
            ))
    return results


_EXTRACTORS = [
    _extract_env_vars,
    _extract_constants,
    _extract_classes,
    _extract_dataclass_fields,
    _extract_functions,
    _extract_class_methods,
    _extract_typed_dict_fields,
    _extract_handler_dict_keys,
    _extract_mcp_tools,
    _extract_slash_commands,
    _extract_cli_commands,
    _extract_cli_routes,
    _extract_literal_types,
    _extract_enum_members,
    _extract_choices_values,
    _extract_contextvar_names,
]


def build_truth_index() -> TruthIndex:
    """Walk all Python source files and extract every identifier into the index."""
    index = TruthIndex()
    for py_file in sorted(SOURCE_DIR.rglob("*.py")):
        source = py_file.read_text()
        tree = ast.parse(source, filename=str(py_file))
        path = _rel_path(py_file)
        for extractor in _EXTRACTORS:
            for ident in extractor(tree, path):
                index.add(ident)
    return index


# ---------------------------------------------------------------------------
# MDX Doc Parser
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DocIdentifier:
    term: str
    classification: str
    line: int
    page: str


# Strip fenced code blocks (``` ... ```) to avoid checking example code
_CODE_BLOCK_RE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
# Match inline backtick terms
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
# Strip YAML frontmatter
_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)


def _classify_term(term: str) -> str:
    """Classify a backtick-quoted term from MDX into a category."""
    # Skip terms in allowlist (also check without trailing "()")
    if term in ALLOWLIST:
        return "skip"
    if term.endswith("()") and term[:-2] in ALLOWLIST:
        return "skip"

    # URLs
    if term.startswith("http://") or term.startswith("https://"):
        return "skip"

    # File paths
    if term.startswith("~/") or term.startswith("./") or term.startswith("../"):
        return "file_path"
    if term.startswith("~/.ollim-bot"):
        return "file_path"

    # Multi-word commands or phrases (contain spaces)
    if " " in term:
        return "skip"

    # Key: value pairs (mini-YAML in prose)
    if ":" in term and not term.startswith("/") and not term.startswith("-"):
        # But allow prompt tags like [routine:ID]
        if term.startswith("[") and term.endswith("]"):
            return "prompt_tag"
        return "skip"

    # Assignment expressions
    if "=" in term:
        return "skip"

    # Path-like terms with / that aren't slash commands
    if "/" in term and not term.startswith("/"):
        return "file_path"

    # Slash commands: /clear, /compact, etc.
    if re.match(r"^/[a-z][a-z0-9-]*$", term):
        return "slash_command"

    # CLI flags: --flag-name, -m (but not -2, -3 which are numeric)
    if term.startswith("--"):
        return "cli_flag"
    if term.startswith("-") and len(term) == 2 and term[1].isalpha():
        return "cli_flag"

    # SCREAMING_CASE: env vars or constants
    if re.match(r"^_?[A-Z][A-Z0-9_]+$", term):
        return "env_var_or_constant"

    # PascalCase: class names
    if re.match(r"^[A-Z][a-zA-Z0-9]+$", term):
        return "class_name"

    # Function calls: name()
    if term.endswith("()") and re.match(r"^_?[a-z][a-z0-9_]*\(\)$", term):
        return "function"

    # Module paths: ollim_bot.config
    if re.match(r"^[a-z_][a-z0-9_.]+$", term) and "." in term:
        return "module_path"

    # snake_case: could be field, function, CLI subcommand
    if re.match(r"^[a-z][a-z0-9_]*$", term):
        if term in _COMMON_WORDS:
            return "skip"
        return "snake_case"

    # Quoted string values (without actual quotes — just the value)
    # These are things like "on_ping", "always", etc.

    # Numeric values
    if re.match(r"^\d", term):
        return "skip"

    # Glob patterns
    if "*" in term:
        return "skip"

    return "general"


def extract_doc_identifiers(page_path: Path) -> list[DocIdentifier]:
    """Extract all inline backtick-quoted terms from an MDX page."""
    text = page_path.read_text()
    page = str(page_path.relative_to(DOCS_ROOT))

    # Strip frontmatter
    text = _FRONTMATTER_RE.sub("", text)

    # Remove fenced code blocks (these are examples, not claims)
    text_no_blocks = _CODE_BLOCK_RE.sub("", text)

    results: list[DocIdentifier] = []
    for match in _INLINE_CODE_RE.finditer(text_no_blocks):
        term = match.group(1).strip()
        if not term:
            continue
        classification = _classify_term(term)
        # Compute line number from the position in the ORIGINAL text
        # (approximate — we stripped code blocks)
        line = text_no_blocks[:match.start()].count("\n") + 1
        results.append(DocIdentifier(
            term=term,
            classification=classification,
            line=line,
            page=page,
        ))
    return results


# ---------------------------------------------------------------------------
# Cross-Reference Engine
# ---------------------------------------------------------------------------

@dataclass
class PageResult:
    page: str
    confirmed: list[tuple[DocIdentifier, SourceIdentifier]]
    unresolved: list[DocIdentifier]
    skipped: int
    file_paths: list[DocIdentifier]


def _lookup(term: str, classification: str, index: TruthIndex) -> SourceIdentifier | None:
    """Try to find a term in the truth index, with category-aware normalization."""

    # Direct lookup
    if index.contains(term):
        return index.identifiers[term][0]

    # Function: strip ()
    if classification == "function" and term.endswith("()"):
        bare = term[:-2]
        if index.contains(bare):
            return index.identifiers[bare][0]

    # SCREAMING_CASE: try with/without leading underscore
    if classification == "env_var_or_constant":
        if term.startswith("_") and index.contains(term[1:]):
            return index.identifiers[term[1:]][0]
        if not term.startswith("_") and index.contains(f"_{term}"):
            return index.identifiers[f"_{term}"][0]

    # snake_case: check as dataclass field, function, CLI subcommand, enum value,
    # choice value, literal type value, contextvar
    if classification == "snake_case":
        if index.contains(term):
            return index.identifiers[term][0]

    # Slash command normalization: /ping-budget -> try ping-budget
    if classification == "slash_command":
        without_slash = term.lstrip("/")
        with_slash = f"/{without_slash}"
        if index.contains(with_slash):
            return index.identifiers[with_slash][0]
        if index.contains(without_slash):
            return index.identifiers[without_slash][0]

    # CLI flag: direct match
    if classification == "cli_flag" and index.contains(term):
        return index.identifiers[term][0]

    # Class name: direct match
    if classification == "class_name" and index.contains(term):
        return index.identifiers[term][0]

    return None


def verify_page(page_path: Path, index: TruthIndex) -> PageResult:
    """Cross-reference a single page's identifiers against the truth index."""
    doc_ids = extract_doc_identifiers(page_path)
    confirmed: list[tuple[DocIdentifier, SourceIdentifier]] = []
    unresolved: list[DocIdentifier] = []
    skipped = 0
    file_paths: list[DocIdentifier] = []

    for doc_id in doc_ids:
        if doc_id.classification == "skip":
            skipped += 1
            continue
        if doc_id.classification == "file_path":
            file_paths.append(doc_id)
            continue
        if doc_id.classification in ("prompt_tag", "module_path", "general"):
            skipped += 1
            continue

        match = _lookup(doc_id.term, doc_id.classification, index)
        if match:
            confirmed.append((doc_id, match))
        else:
            unresolved.append(doc_id)

    return PageResult(
        page=str(page_path.relative_to(DOCS_ROOT)),
        confirmed=confirmed,
        unresolved=unresolved,
        skipped=skipped,
        file_paths=file_paths,
    )


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(results: list[PageResult], *, verbose: bool = False) -> int:
    """Print results and return exit code (0=clean, 1=issues)."""
    total_unresolved = 0
    total_confirmed = 0
    pages_with_issues = 0

    for result in sorted(results, key=lambda r: r.page):
        n_confirmed = len(result.confirmed)
        n_unresolved = len(result.unresolved)
        total_unresolved += n_unresolved
        total_confirmed += n_confirmed

        if n_unresolved > 0:
            pages_with_issues += 1

        if n_unresolved == 0 and not verbose:
            continue

        status = "WARN" if n_unresolved > 0 else "  OK"
        print(f"[{status}] {result.page}: "
              f"{n_confirmed} confirmed, {n_unresolved} unresolved, "
              f"{result.skipped} skipped")

        if n_unresolved > 0:
            for doc_id in result.unresolved:
                print(f"       ? line {doc_id.line}: `{doc_id.term}` "
                      f"({doc_id.classification})")

        if verbose and n_confirmed > 0:
            for doc_id, src in result.confirmed:
                print(f"       + line {doc_id.line}: `{doc_id.term}` "
                      f"-> {src.source_file}:{src.line} ({src.category})")

    print(f"\n{'='*60}")
    print(f"Total: {total_confirmed} confirmed, {total_unresolved} unresolved "
          f"across {len(results)} pages")
    if pages_with_issues:
        print(f"Pages with issues: {pages_with_issues}")
    return 1 if total_unresolved > 0 else 0


def dump_index(index: TruthIndex) -> None:
    """Dump truth index as JSON for debugging."""
    output: dict[str, list[dict[str, str | int]]] = {}
    for name, idents in sorted(index.identifiers.items()):
        output[name] = [
            {
                "category": i.category,
                "source_file": i.source_file,
                "line": i.line,
            }
            for i in idents
        ]
    json.dump(output, sys.stdout, indent=2)
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify docs against source code truth index"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show per-identifier detail")
    parser.add_argument("--page", type=str,
                        help="Verify a single page (relative path)")
    parser.add_argument("--dump-index", action="store_true",
                        help="Dump truth index as JSON and exit")
    args = parser.parse_args()

    if not SOURCE_DIR.is_dir():
        print(f"Source directory not found: {SOURCE_DIR}", file=sys.stderr)
        sys.exit(1)

    index = build_truth_index()

    if args.dump_index:
        dump_index(index)
        return

    if args.page:
        page_path = DOCS_ROOT / args.page
        if not page_path.exists():
            print(f"Page not found: {page_path}", file=sys.stderr)
            sys.exit(1)
        results = [verify_page(page_path, index)]
    else:
        pages = sorted(DOCS_ROOT.rglob("*.mdx"))
        results = [verify_page(p, index) for p in pages]

    exit_code = print_report(results, verbose=args.verbose)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
