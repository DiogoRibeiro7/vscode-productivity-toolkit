#!/usr/bin/env bash
# MIT License
# Copyright (c) 2025 Diogo Ribeiro
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_ROOT="${PROJECT_ROOT}"
REMOTE_BASE_URL=""
DRY_RUN=false
SILENT=false
VERBOSE=false
SKIP_EXTENSIONS=false
CATEGORY_ARGUMENTS=()

LOG_FILE="${TMPDIR:-/tmp}/vscode-toolkit-install.log"

log() {
  local level="$1"; shift
  local message="$*"
  local timestamp
  timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  if [[ "${level}" == "DEBUG" && "${VERBOSE}" != true ]]; then
    return
  fi
  local payload
  payload=$(printf '{"timestamp":"%s","level":"%s","message":"%s"}' "${timestamp}" "${level}" "${message//"/\"}")
  if [[ "${level}" == "ERROR" ]]; then
    >&2 echo "${payload}"
  else
    echo "${payload}"
  fi
  printf '%s\n' "${payload}" >> "${LOG_FILE}"
}

print_usage() {
  cat <<'USAGE'
Usage: install.sh [options]

Options:
  --categories <list>   Comma-separated category identifiers.
  --source-root <path>  Local repository root containing task definitions.
  --remote-base-url <u> Base URL for downloading task files.
  --dry-run             Perform a trial run without modifying files.
  --silent              Run without interactive prompts (requires categories or defaults to all).
  --verbose             Enable verbose logging.
  --skip-extensions     Do not install recommended extensions.
  -h, --help            Show this help message.
USAGE
}

ensure_command() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    log "ERROR" "Required command '${cmd}' is not available."
    return 1
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --categories)
        CATEGORY_ARGUMENTS+=("$2")
        shift 2
        ;;
      --source-root)
        SOURCE_ROOT="$2"
        shift 2
        ;;
      --remote-base-url)
        REMOTE_BASE_URL="$2"
        shift 2
        ;;
      --dry-run)
        DRY_RUN=true
        shift
        ;;
      --silent)
        SILENT=true
        shift
        ;;
      --verbose)
        VERBOSE=true
        shift
        ;;
      --skip-extensions)
        SKIP_EXTENSIONS=true
        shift
        ;;
      -h|--help)
        print_usage
        exit 0
        ;;
      *)
        log "ERROR" "Unknown option: $1"
        print_usage
        exit 1
        ;;
    esac
  done
}

category_map() {
  local root="$1"
  cat <<EOF
python-general|Python – General|Quality, packaging, docker, and git automation.|${root}/tasks/python/general.json
python-data-science|Python – Data Science|Notebook conversion, profiling, Sphinx documentation.|${root}/tasks/python/data-science.json
javascript-general|JavaScript/TypeScript – General|Linting, dependency hygiene, documentation.|${root}/tasks/javascript/general.json
javascript-node|Node.js Services|Express workflows, migrations, API testing, publishing.|${root}/tasks/javascript/node.json
javascript-react|React Applications|Component scaffolding, Storybook, bundle analysis, PWA audits.|${root}/tasks/javascript/react.json
EOF
}

select_categories() {
  local map_entries
  IFS=$'\n' read -rd '' -a map_entries <<< "$(category_map "${SOURCE_ROOT}")" || true

  if [[ ${#CATEGORY_ARGUMENTS[@]} -gt 0 ]]; then
    local requested
    IFS=',' read -ra requested <<< "${CATEGORY_ARGUMENTS[*]}"
    local normalized=()
    for value in "${requested[@]}"; do
      normalized+=("$(echo "${value}" | tr '[:upper:]' '[:lower:]')")
    done
    local selection=()
    for entry in "${map_entries[@]}"; do
      local key
      IFS='|' read -r key _ <<< "${entry}"
      if printf '%s\n' "${normalized[@]}" | grep -qx "${key}"; then
        selection+=("${entry}")
      fi
    done
    if [[ ${#selection[@]} -eq 0 ]]; then
      log "ERROR" "No valid categories specified."
      exit 1
    fi
    printf '%s\n' "${selection[@]}"
    return
  fi

  if [[ "${SILENT}" == true ]]; then
    printf '%s\n' "${map_entries[@]}"
    return
  fi

  echo
  echo "VS Code Productivity Toolkit Installer"
  echo "Select the task categories to install:"
  local idx=1
  for entry in "${map_entries[@]}"; do
    IFS='|' read -r _ label description _ <<< "${entry}"
    printf '[%d] %s - %s\n' "${idx}" "${label}" "${description}"
    ((idx++))
  done
  echo "[A] All categories"
  echo

  while true; do
    printf 'Enter a comma-separated list (e.g. 1,3) or A for all: '
    IFS= read -r response
    if [[ -z "${response}" ]]; then
      continue
    fi
    if [[ "${response}" =~ ^[Aa]$ ]]; then
      printf '%s\n' "${map_entries[@]}"
      return
    fi
    IFS=',' read -ra indices <<< "${response}"
    local selection=""
    local valid=true
    for value in "${indices[@]}"; do
      value="$(echo "${value}" | xargs)"
      if [[ ! "${value}" =~ ^[0-9]+$ ]]; then
        log "WARN" "Unable to parse selection '${value}'."
        valid=false
        break
      fi
      local position=$((value))
      if (( position < 1 || position > ${#map_entries[@]} )); then
        log "WARN" "Selection '${value}' is out of range."
        valid=false
        break
      fi
      selection+="${map_entries[$((position-1))]}\n"
    done
    if [[ "${valid}" == true && -n "${selection}" ]]; then
      printf '%s' "${selection}" | sort -u
      return
    fi
    echo "Please enter a valid selection."
  done
}

ensure_vscode_cli() {
  if command -v code >/dev/null 2>&1; then
    echo "code"
    return
  fi
  if [[ -n "${TOOLKIT_CODE_PATH:-}" && -x "${TOOLKIT_CODE_PATH}" ]]; then
    echo "${TOOLKIT_CODE_PATH}"
    return
  fi
  log "ERROR" "VS Code command line interface not found. Enable the 'code' command and retry."
  exit 1
}

ensure_vscode_dir() {
  local dir
  dir="$HOME/.vscode"
  if [[ ! -d "${dir}" && "${DRY_RUN}" != true ]]; then
    mkdir -p "${dir}"
  fi
  echo "${dir}"
}

fetch_task_file() {
  local entry="$1"
  IFS='|' read -r key _ _ path <<< "${entry}"
  if [[ -n "${REMOTE_BASE_URL}" ]]; then
    local relative
    relative="${path#${SOURCE_ROOT}/}"
    relative="${relative#./}"
    local url
    url="${REMOTE_BASE_URL%/}/${relative// /%20}"
    log "INFO" "Downloading task definition from ${url}."
    local tmp
    tmp="$(mktemp)"
    if command -v curl >/dev/null 2>&1; then
      if ! curl -fsSL --max-time 60 "${url}" -o "${tmp}"; then
        log "ERROR" "Failed to download ${url}."
        rm -f "${tmp}"
        exit 1
      fi
    elif command -v wget >/dev/null 2>&1; then
      if ! wget -q -O "${tmp}" "${url}"; then
        log "ERROR" "Failed to download ${url}."
        rm -f "${tmp}"
        exit 1
      fi
    else
      log "ERROR" "Neither curl nor wget is available for downloads."
      rm -f "${tmp}"
      exit 1
    fi
    echo "${tmp}"
  else
    if [[ ! -f "${path}" ]]; then
      log "ERROR" "Task definition not found at ${path}."
      exit 1
    fi
    echo "${path}"
  fi
}

python_bin() {
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
  elif command -v python >/dev/null 2>&1; then
    echo "python"
  else
    log "ERROR" "Python is required for this installer."
    exit 1
  fi
}

merge_tasks() {
  local output_path="$1"
  local existing_path="$2"
  shift 2
  local -a sources=("$@")
  local py
  py="$(python_bin)"
  "${py}" <<'PYTHON'
import json
import sys
from pathlib import Path

output_path = Path(sys.argv[1])
existing_path = Path(sys.argv[2])
sources = [Path(p) for p in sys.argv[3:]]

schema = "https://raw.githubusercontent.com/microsoft/vscode/master/src/vs/workbench/contrib/tasks/common/tasks.schema.json"
aggregate = {
    "version": "2.0.0",
    "inputs": [],
    "tasks": [],
    "problemMatchers": [],
    "_toolkitMetadata": []
}

seen_inputs = set()
seen_tasks = set()
seen_matchers = set()
seen_metadata = set()

def _ingest(config):
    global schema
    if "$schema" in config:
        schema = config.get("$schema", schema)
    if "version" in config:
        aggregate["version"] = config.get("version", aggregate["version"])
    for bucket, seen, key in (
        ("inputs", seen_inputs, "id"),
        ("tasks", seen_tasks, "label"),
        ("problemMatchers", seen_matchers, "name")
    ):
        for item in config.get(bucket, []) or []:
            identifier = item.get(key) if isinstance(item, dict) else None
            if identifier and identifier in seen:
                continue
            if identifier:
                seen.add(identifier)
            aggregate[bucket].append(item)
    metadata = config.get("_metadata")
    if metadata:
        items = metadata if isinstance(metadata, list) else [metadata]
        for item in items:
            serialized = json.dumps(item, sort_keys=True)
            if serialized in seen_metadata:
                continue
            seen_metadata.add(serialized)
            aggregate["_toolkitMetadata"].append(item)

if existing_path.exists():
    try:
        with existing_path.open("r", encoding="utf-8") as handle:
            existing = json.load(handle)
        _ingest(existing)
    except Exception:
        pass

for source in sources:
    with source.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    _ingest(data)

result = {"$schema": schema, "version": aggregate["version"]}
for key in ("inputs", "tasks", "problemMatchers", "_toolkitMetadata"):
    if aggregate[key]:
        result[key] = aggregate[key]

output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open("w", encoding="utf-8") as handle:
    json.dump(result, handle, indent=2)
    handle.write("\n")
PYTHON
}

install_extensions() {
  local extensions_file="$1"
  local code_cli="$2"
  if [[ "${SKIP_EXTENSIONS}" == true ]]; then
    log "INFO" "Skipping extension installation as requested."
    return
  fi
  if [[ ! -f "${extensions_file}" ]]; then
    log "WARN" "Extensions configuration not found at ${extensions_file}."
    return
  fi
  local py
  py="$(python_bin)"
  local ids
  ids=$("${py}" <<'PYTHON'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
for item in data.get("recommendations", []):
    if item:
        print(item)
PYTHON
"${extensions_file}")
  while IFS= read -r extension; do
    [[ -z "${extension}" ]] && continue
    if [[ "${DRY_RUN}" == true ]]; then
      log "INFO" "[Dry Run] Would install extension ${extension}."
      continue
    fi
    if "${code_cli}" --install-extension "${extension}" --force >/dev/null 2>&1; then
      log "INFO" "Ensured extension ${extension} is installed."
    else
      log "WARN" "Failed to install extension ${extension}."
    fi
  done <<< "${ids}"
}

copy_with_backup() {
  local source="$1"
  local destination="$2"
  local message="$3"
  if [[ -f "${destination}" ]]; then
    local backup
    backup="${destination}.bak.$(date +%s)"
    if [[ "${DRY_RUN}" != true ]]; then
      cp "${destination}" "${backup}"
    fi
    log "DEBUG" "Backed up $(basename "${destination}") to ${backup}."
  fi
  if [[ "${DRY_RUN}" != true ]]; then
    cp "${source}" "${destination}"
  fi
  log "INFO" "${message}"
}

validate_tasks() {
  local path="$1"
  local py
  py="$(python_bin)"
  if "${py}" <<'PYTHON'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
with path.open("r", encoding="utf-8") as handle:
    data = json.load(handle)
if not data.get("tasks"):
    sys.exit(2)
PYTHON
"${path}" >/dev/null 2>&1; then
    log "INFO" "VS Code tasks.json validated successfully."
  else
    log "WARN" "tasks.json validation encountered an issue; please verify manually."
  fi
}

main() {
  parse_args "$@"

  SOURCE_ROOT="$(cd "${SOURCE_ROOT}" && pwd)"

  local code_cli
  code_cli="$(ensure_vscode_cli)"
  log "DEBUG" "VS Code CLI resolved to ${code_cli}."

  local vscode_dir
  vscode_dir="$(ensure_vscode_dir)"

  mapfile -t selected < <(select_categories)
  if [[ ${#selected[@]} -eq 0 ]]; then
    log "ERROR" "No categories selected; installation aborted."
    exit 1
  fi

  local tasks_file="${vscode_dir}/tasks.json"
  local backup=""
  if [[ -f "${tasks_file}" ]]; then
    backup="${tasks_file}.bak.$(date +%s)"
    if [[ "${DRY_RUN}" != true ]]; then
      cp "${tasks_file}" "${backup}"
    fi
    log "INFO" "Existing tasks.json backed up to ${backup}."
  fi

  local -a temp_files=()
  for entry in "${selected[@]}"; do
    temp_files+=("$(fetch_task_file "${entry}")")
  done

  if [[ "${DRY_RUN}" == true ]]; then
    log "INFO" "[Dry Run] Would merge ${#temp_files[@]} task collections."
  else
    merge_tasks "${tasks_file}" "${tasks_file}" "${temp_files[@]}"
    log "INFO" "tasks.json updated with selected categories."
  fi

  local settings_dir="${SOURCE_ROOT}/settings"
  if [[ -d "${settings_dir}" ]]; then
    for name in settings.json keybindings.json extensions.json; do
      local source_file="${settings_dir}/${name}"
      [[ -f "${source_file}" ]] || continue
      local destination="${vscode_dir}/${name}"
      copy_with_backup "${source_file}" "${destination}" "${name} synchronized to ${destination}."
    done
  fi

  install_extensions "${settings_dir}/extensions.json" "${code_cli}"

  if [[ "${DRY_RUN}" != true ]]; then
    validate_tasks "${tasks_file}"
  fi

  log "INFO" "VS Code productivity toolkit installation complete."
}

main "$@"
