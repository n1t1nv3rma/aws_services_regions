# MCP server to provide accurate information on AWS Services and Regions
Fast MCP server that helps LLMs to optimally and accurately find list of all AWS services available in AWS regions. 

It has comprehensive information about AWS services and regions. It can help your LLM with any specific questions about AWS Services or Regions. For example:

1. Which AWS services are available in specific regions
2. Which regions support specific AWS services
3. When services were launched in specific regions
4. Information about AWS Local Zones and their parent regions
5. The latest AWS service launches
6. Comparing service availability across regions
7. Finding regions with the most or least services
8. Identifying which services are globally available vs. regionally restricted

For example, it can tell LLMs that (snapshot taken 2026-09-17 — the server always serves live data, so these figures move):

* US East (N. Virginia/us-east-1) has the most AWS services available (390)
* AWS IAM, CloudWatch, EC2, and S3 are available in all 39 AWS regions
* The newest AWS region appears to be AWS European Sovereign Cloud (Germany/eusc-de-east-1)
* There are 35 AWS Local Zones connected to parent regions
* Some services like Amazon Q Developer are only available in 4 regions

# How to Setup 

## Prerequisites

* [uv](https://docs.astral.sh/uv/getting-started/installation/) — runs the server and resolves its dependencies from `uv.lock`.
* Python 3.10 or newer. `uv` downloads a suitable interpreter for you if you don't have one.

## Clone this repo

```
git clone https://github.com/n1t1nv3rma/aws_services_regions.git
```

Take note of the absolute path to your clone — every config below needs it.

## Configure your MCP client

Every client below uses the same invocation: `uv run --directory <repo> main.py`. Dependencies come from the repo's `pyproject.toml` and `uv.lock`, so there is nothing to `pip install` by hand and no `--with` flags to keep in sync as the SDK evolves.

In each snippet, replace `/absolute/path/to/aws_services_regions` with your clone path, and check that `command` matches your `uv` location (`which uv`).

### For Kiro:

Save below information in the global "~/.kiro/settings/mcp.json" or in the per-workspace ".kiro/settings/mcp.json"
```json
{
  "mcpServers": {
    "awsrands": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/aws_services_regions",
        "main.py"
      ],
      "autoApprove": [
        "aws_services",
        "aws_regions",
        "aws_regions_for_service",
        "aws_services_in_region",
        "aws_localzones",
        "aws_latest_services"
      ],
      "env": {},
      "timeout": 120000,
      "disabled": false
    }
  }
}
```

Every tool is a read-only HTTP GET against a public site, so listing all six under `autoApprove` is safe. Drop the key if you would rather confirm each call.

### For Amazon Q CLI:

Save below information in the local ".amazonq/mcp.json" or in global "~/.aws/amazonq/mcp.json"
```json
{
  "mcpServers": {
    "awsrands": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/aws_services_regions",
        "main.py"
      ],
      "env": {},
      "timeout": 120000,
      "disabled": false
    }
  }
}
```

### For Claude Desktop:

Save below information in the local "claude_desktop_config.json"
```json
{
  "mcpServers": {
    "awsrands": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/aws_services_regions",
        "main.py"
      ]
    }
  }
}
```

## SDK compatibility

This server targets the `mcp` Python SDK 2.x (`MCPServer`, formerly `FastMCP`). If you are pinned to `mcp` 1.x, use a release of this repo from before the 2.x migration — the 1.x import path `mcp.server.fastmcp` no longer exists in 2.x, and 2.x dropped `httpx` in favour of `httpx2`, so `httpx` is now declared as a direct dependency here.

# Sample Run

% q
✓ awsrands loaded in 0.69 s

    ⢠⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣶⣦⡀⠀
 ⠀⠀⠀⣾⡿⢻⣿⡆⠀⠀⠀⢀⣄⡄⢀⣠⣤⣤⡀⢀⣠⣤⣤⡀⠀⠀⢀⣠⣤⣤⣤⣄⠀⠀⢀⣤⣤⣤⣤⣤⣤⡀⠀⠀⣀⣤⣤⣤⣀⠀⠀⠀⢠⣤⡀⣀⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⢠⣿⣿⠋⠀⠀⠀⠙⣿⣿⡆
 ⠀⠀⣼⣿⠇⠀⣿⣿⡄⠀⠀⢸⣿⣿⠛⠉⠻⣿⣿⠛⠉⠛⣿⣿⠀⠀⠘⠛⠉⠉⠻⣿⣧⠀⠈⠛⠛⠛⣻⣿⡿⠀⢀⣾⣿⠛⠉⠻⣿⣷⡀⠀⢸⣿⡟⠛⠉⢻⣿⣷⠀⠀⠀⠀⠀⠀⣼⣿⡏⠀⠀⠀⠀⠀⢸⣿⣿
 ⠀⢰⣿⣿⣤⣤⣼⣿⣷⠀⠀⢸⣿⣿⠀⠀⠀⣿⣿⠀⠀⠀⣿⣿⠀⠀⢀⣴⣶⣶⣶⣿⣿⠀⠀⠀⣠⣾⡿⠋⠀⠀⢸⣿⣿⠀⠀⠀⣿⣿⡇⠀⢸⣿⡇⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⢹⣿⣇⠀⠀⠀⠀⠀⢸⣿⡿
 ⢀⣿⣿⠋⠉⠉⠉⢻⣿⣇⠀⢸⣿⣿⠀⠀⠀⣿⣿⠀⠀⠀⣿⣿⠀⠀⣿⣿⡀⠀⣠⣿⣿⠀⢀⣴⣿⣋⣀⣀⣀⡀⠘⣿⣿⣄⣀⣠⣿⣿⠃⠀⢸⣿⡇⠀⠀⢸⣿⣿⠀⠀⠀⠀⠀⠀⠈⢿⣿⣦⣀⣀⣀⣴⣿⡿⠃
 ⠚⠛⠋⠀⠀⠀⠀⠘⠛⠛⠀⠘⠛⠛⠀⠀⠀⠛⠛⠀⠀⠀⠛⠛⠀⠀⠙⠻⠿⠟⠋⠛⠛⠀⠘⠛⠛⠛⠛⠛⠛⠃⠀⠈⠛⠿⠿⠿⠛⠁⠀⠀⠘⠛⠃⠀⠀⠘⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠿⢿⣿⣿⣋⠀⠀
 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⢿⡧

╭─────────────────────────────── Did you know? ────────────────────────────────╮
│                                                                              │
│   Q can use tools without asking for confirmation every time. Give /tools    │
│                                 trust a try                                  │
│                                                                              │
╰──────────────────────────────────────────────────────────────────────────────╯

/help all commands  •  ctrl + j new lines  •  ctrl + s fuzzy search
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 You are chatting with claude-3.7-sonnet


> /tools


Tool                                    Permission
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔

Built-in:
- execute_bash                          * trust read-only commands
- fs_read                               * trusted
- fs_write                              * not trusted
- report_issue                          * trusted
- use_aws                               * trust read-only commands

awsrands (MCP):
- awsrands___aws_latest_services                              * not trusted
- awsrands___aws_localzones                                   * not trusted
- awsrands___aws_regions                                        trusted
- awsrands___aws_regions_for_service                            trusted
- awsrands___aws_services                                       trusted
- awsrands___aws_services_in_region                             trusted


# Master prompt - start with this:

"You have all the tools which can help you find out what AWS services are available in which regions or vice-versa. You can run recursive queries against the URI or URL in the initial response to further find out details on launch date of service in a region. Use your tools to solve all AWS regions or service related queries."
