.. _tips_and_tricks:

Tips and Tricks
==============

This page provides advanced tips, tricks, and best practices to help you get the most out of promptprep.

Optimizing for AI Models
-----------------------

When preparing code for AI models like GPT-4:

1. **Use Markdown Format**

   Markdown format works best with AI models as it preserves syntax highlighting:

   .. code-block:: bash

      promptprep --format markdown -c

2. **Monitor Token Usage**

   Stay within context limits by monitoring token usage:

   .. code-block:: bash

      promptprep --metadata --count-tokens --format markdown -c

3. **Focus on Relevant Files**

   Only include files that are relevant to your question:

   .. code-block:: bash

      promptprep -i "src/problematic_file.py,src/related_file.py" -c

4. **Use Summary Mode for Large Codebases**

   For large projects, use summary mode to extract only signatures and docstrings:

   .. code-block:: bash

      promptprep --summary-mode --format markdown -c

5. **Strip Comments When Needed**

   If you're approaching token limits, consider stripping comments:

   .. code-block:: bash

      promptprep --no-include-comments --format markdown -c

Performance Optimization
----------------------

For large codebases:

1. **Use Incremental Processing**

   Only process files that have changed:

   .. code-block:: bash

      promptprep --incremental -o updated_output.txt

2. **Filter by Extension**

   Focus on specific file types:

   .. code-block:: bash

      promptprep -x ".py,.js" -o filtered_output.txt

3. **Exclude Large Directories**

   Skip directories that contain many files:

   .. code-block:: bash

      promptprep -e "node_modules,venv,build,dist" -o smaller_output.txt

4. **Limit File Size**

   Reduce the maximum file size to skip large files:

   .. code-block:: bash

      promptprep -m 1 -o no_large_files.txt  # Skip files larger than 1MB

5. **Combine Filtering Techniques**

   Use multiple filters together:

   .. code-block:: bash

      promptprep -x ".py" -e "tests,venv" -m 1 -o optimized.txt

Workflow Integration
------------------

Integrate promptprep into your development workflow:

1. **Git Hooks**

   Create a pre-commit hook to generate code snapshots:

   .. code-block:: bash

      # In .git/hooks/pre-commit
      #!/bin/bash
      promptprep -d . --incremental -o snapshots/$(date +%Y%m%d_%H%M%S).md

2. **Alias Commands**

   Create shell aliases for common operations:

   .. code-block:: bash

      # In .bashrc or .zshrc
      alias pp-ai="promptprep --format markdown --metadata --count-tokens -c"
      alias pp-docs="promptprep --format highlighted -o docs/code_snapshot.html"

3. **Continuous Integration**

   Add promptprep to your CI pipeline:

   .. code-block:: yaml

      # In .github/workflows/snapshot.yml
      jobs:
        snapshot:
          runs-on: ubuntu-latest
          steps:
            - uses: actions/checkout@v3
            - uses: actions/setup-python@v4
              with:
                python-version: '3.10'
            - run: pip install promptprep
            - run: promptprep -d . --metadata -o snapshot.md

4. **Documentation Generation**

   Automatically update documentation:

   .. code-block:: bash

      # In your documentation build script
      promptprep -d ./src --summary-mode --format markdown -o docs/api_overview.md

5. **Diff Reports**

   Generate diff reports between branches:

   .. code-block:: bash

      # Save main branch snapshot
      git checkout main
      promptprep -d . -o main_snapshot.txt
      
      # Compare feature branch
      git checkout feature-branch
      promptprep -d . --diff main_snapshot.txt -o changes.txt

Advanced Selection Techniques
---------------------------

Fine-tune which files are included:

1. **Combine Interactive and Extension Filtering**

   Pre-filter by extension, then select interactively:

   .. code-block:: bash

      promptprep -x ".py,.js" --interactive -o selected.txt

2. **Use Glob Patterns with Include Files**

   Use shell expansion for file patterns:

   .. code-block:: bash

      promptprep -i "$(find src -name "*.py" | tr '\n' ',')" -o python_files.txt

3. **Exclude by Pattern**

   Exclude files matching certain patterns:

   .. code-block:: bash

      promptprep -e "$(find . -name "*_test.py" -o -name "test_*.py" | xargs dirname | sort -u | tr '\n' ',')" -o no_tests.txt

4. **Select by Modification Time**

   Focus on recently modified files:

   .. code-block:: bash

      promptprep -i "$(find . -type f -mtime -7 | tr '\n' ',')" -o recent_changes.txt

5. **Combine with grep**

   Select files containing specific text:

   .. code-block:: bash

      promptprep -i "$(grep -l "TODO" --include="*.py" -r . | tr '\n' ',')" -o todos.txt

Custom Output Strategies
----------------------

Customize your output for different purposes:

1. **Create Custom Templates for Different Audiences**

   Maintain different templates for different needs:

   .. code-block:: bash

      promptprep --format custom --template-file templates/for_ai.txt -o for_ai.txt
      promptprep --format custom --template-file templates/for_docs.txt -o for_docs.txt

2. **Generate Multiple Formats at Once**

   Create a script to generate multiple formats:

   .. code-block:: bash

      #!/bin/bash
      promptprep -d . -o output.txt
      promptprep -d . --format markdown -o output.md
      promptprep -d . --format highlighted -o output.html

3. **Create Focused Reports**

   Generate reports for specific components:

   .. code-block:: bash

      for dir in src/*/ ; do
          promptprep -d "$dir" --metadata -o "reports/$(basename $dir).md"
      done

4. **Combine with Other Tools**

   Pipe output to other tools:

   .. code-block:: bash

      promptprep -c | pbcopy  # macOS
      promptprep -c | xclip -selection clipboard  # Linux

5. **Create Comparative Views**

   Generate side-by-side comparisons:

   .. code-block:: bash

      # Generate HTML with both the full code and summary
      promptprep -d . --format html -o full.html
      promptprep -d . --summary-mode --format html -o summary.html
      echo "<frameset cols=\"50%,50%\"><frame src=\"full.html\"><frame src=\"summary.html\"></frameset>" > comparison.html

Troubleshooting Common Issues
---------------------------

Solutions to common problems:

1. **Files Not Being Included**

   Check file paths and patterns:

   .. code-block:: bash

      # List all files that would be included
      find . -type f -not -path "*/\.*" | grep -v -E "(__pycache__|node_modules|venv)"

2. **Output Too Large**

   Reduce output size:

   .. code-block:: bash

      # Use summary mode
      promptprep --summary-mode -o smaller.txt
      
      # Exclude comments
      promptprep --no-include-comments -o no_comments.txt
      
      # Focus on specific directories
      promptprep -d ./src/core -o core_only.txt

3. **Slow Performance**

   Improve performance:

   .. code-block:: bash

      # Use incremental processing
      promptprep --incremental -o faster.txt
      
      # Exclude large directories
      promptprep -e "node_modules,venv,data,logs" -o faster.txt

4. **Encoding Issues**

   Handle non-standard encodings:

   .. code-block:: bash

      # Convert files to UTF-8 first
      find . -type f -name "*.py" -exec iconv -f ISO-8859-1 -t UTF-8 {} -o {}.utf8 \;
      find . -type f -name "*.py.utf8" -exec mv {} {} \;

5. **Line Ending Issues**

   Normalize line endings:

   .. code-block:: bash

      # Convert to Unix line endings
      find . -type f -name "*.py" -exec dos2unix {} \;

Advanced Configuration Management
-------------------------------

Master configuration management:

1. **Project-Specific Configurations**

   Create configurations for different projects:

   .. code-block:: bash

      # For frontend code
      promptprep -d ./frontend -x ".js,.ts,.jsx,.tsx" --save-config frontend.json
      
      # For backend code
      promptprep -d ./backend -x ".py,.sql" --save-config backend.json

2. **Layered Configurations**

   Combine multiple configurations:

   .. code-block:: bash

      # Base configuration
      promptprep --load-config base.json --format markdown -o output.md

3. **Environment-Specific Configurations**

   Use different configurations based on environment:

   .. code-block:: bash

      # In your script
      if [ "$ENV" = "dev" ]; then
          CONFIG="dev.json"
      else
          CONFIG="prod.json"
      fi
      promptprep --load-config $CONFIG -o output.txt

4. **Share Configurations with Team**

   Include configurations in version control:

   .. code-block:: bash

      # In README.md
      ## Team Configurations
      
      We maintain standard configurations in the `.promptprep` directory.
      Use them with:
      
      ```bash
      promptprep --load-config .promptprep/standard.json
      ```

5. **Document Your Configurations**

   Add comments to your configuration files:

   .. code-block:: json

      {
        "_comment": "Configuration for backend code review",
        "directory": "./backend",
        "extensions": [".py", ".sql"],
        "exclude_dirs": ["tests", "migrations"],
        "format": "highlighted",
        "line_numbers": true
      }