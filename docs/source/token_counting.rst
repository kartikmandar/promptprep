.. _token_counting:

Token Counting
=============

The token counting feature helps you estimate how many tokens your code will use when sent to AI models like GPT-4. This is crucial for staying within context limits and optimizing your interactions with AI models.

Overview
--------

When you run promptprep with the ``--count-tokens`` option (which requires ``--metadata``), it will:

1. Process your code files as usual
2. Count the number of tokens in the aggregated output
3. Include this information in the metadata section

This helps you understand how much of an AI model's context window your code will consume.

What are Tokens?
--------------

Tokens are the basic units that AI models like GPT-4 process text with. A token can be as short as a single character or as long as a word. For English text:

- 1 token ≈ 4 characters
- 1 token ≈ 0.75 words

For code, the tokenization is more complex due to special characters, indentation, and syntax.

Basic Usage
----------

To count tokens in your code:

.. code-block:: bash

   promptprep --metadata --count-tokens [other options]

Example:

.. code-block:: bash

   promptprep -d ./my_project --metadata --count-tokens -o tokenized_output.txt

The output will include token count information in the metadata section:

.. code-block:: text

   # Code Aggregation - my_project
   
   ## Metadata
   
   - Files processed: 10
   - Total lines of code: 1,250
   - Total tokens: 15,678
   - Estimated GPT-4 context usage: 7.8%
   
   ## Directory Structure
   ...

Specifying a Token Model
-----------------------

Different AI models use different tokenizers. By default, promptprep uses the ``cl100k_base`` tokenizer (used by GPT-4), but you can specify a different one with the ``--token-model`` option:

.. code-block:: bash

   promptprep --metadata --count-tokens --token-model MODEL [other options]

Available models:

- ``cl100k_base``: Used by GPT-4 (default)
- ``p50k_base``: Used by GPT-3.5
- ``r50k_base``: Used by earlier GPT models

Example:

.. code-block:: bash

   promptprep -d . --metadata --count-tokens --token-model p50k_base -o gpt35_tokens.txt

Context Window Estimation
------------------------

The metadata includes an estimation of how much of the AI model's context window your code will consume. This is based on the following context window sizes:

- GPT-4: 8,192 tokens (base model) or 32,768 tokens (extended context)
- GPT-3.5: 4,096 tokens

The estimation helps you understand if your code will fit within the model's limits or if you need to reduce the amount of code you're sending.

Optimizing Token Usage
--------------------

If your code exceeds or approaches the token limit, consider these strategies:

1. **Use Summary Mode**: Extract only function/class signatures and docstrings:

   .. code-block:: bash

      promptprep -d . --summary-mode --metadata --count-tokens

2. **Focus on Specific Files**: Include only the most relevant files:

   .. code-block:: bash

      promptprep -i "src/main.py,src/utils.py" --metadata --count-tokens

3. **Exclude Comments**: Strip comments to reduce token count:

   .. code-block:: bash

      promptprep -d . --no-include-comments --metadata --count-tokens

4. **Filter by Extension**: Include only specific file types:

   .. code-block:: bash

      promptprep -d . -x ".py" --metadata --count-tokens

5. **Exclude Directories**: Skip directories that aren't relevant:

   .. code-block:: bash

      promptprep -d . -e "tests,docs,examples" --metadata --count-tokens

Advanced Use Cases
----------------

Working with GPT-4
~~~~~~~~~~~~~~~~

When preparing code for GPT-4, you can optimize for its context window:

.. code-block:: bash

   promptprep -d . --metadata --count-tokens -c

This will copy the output to your clipboard, ready to paste into a GPT-4 conversation, with token count information to help you stay within limits.

Comparing Token Efficiency
~~~~~~~~~~~~~~~~~~~~~~~~~

Compare the token efficiency of different code versions:

.. code-block:: bash

   # Before optimization
   promptprep -d . --metadata --count-tokens -o before.txt

   # After optimization (e.g., removing comments, unused code)
   promptprep -d . --metadata --count-tokens -o after.txt

This helps you see how your optimizations affect token usage.

Project Planning
~~~~~~~~~~~~~~

Use token counting to plan how to split a large project when working with AI models:

.. code-block:: bash

   # Count tokens for each module
   promptprep -d ./module1 --metadata --count-tokens -o module1.txt
   promptprep -d ./module2 --metadata --count-tokens -o module2.txt
   promptprep -d ./module3 --metadata --count-tokens -o module3.txt

This helps you decide which modules can be processed together and which need to be handled separately.

Technical Details
---------------

Token Counting Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

promptprep uses the ``tiktoken`` library from OpenAI to count tokens. This is the same library used by OpenAI's models, so the count should be accurate.

The token counting process:

1. Aggregates all the code into a single text
2. Applies the selected tokenizer
3. Counts the resulting tokens

Dependencies
~~~~~~~~~~

Token counting requires the ``tiktoken`` package, which is included as a dependency when you install promptprep.

Performance Considerations
------------------------

Token counting adds some processing overhead, especially for large codebases. The impact depends on:

- The size of your codebase
- The number of files
- The complexity of the code

For very large projects, token counting might noticeably increase processing time.

Best Practices
-------------

1. **Always Use with Metadata**: The ``--count-tokens`` option requires ``--metadata`` to display the results.

2. **Choose the Right Tokenizer**: Use the tokenizer that matches the AI model you're targeting.

3. **Monitor Context Usage**: Pay attention to the estimated context usage to avoid hitting limits.

4. **Combine with Summary Mode**: For large codebases, use summary mode to reduce token count while preserving structure.

5. **Focus on Relevant Code**: Only include the files that are necessary for your specific question or task.

Troubleshooting
--------------

If token counting isn't working as expected:

1. **Check Dependencies**: Ensure the ``tiktoken`` package is installed.

2. **Verify Metadata Option**: Make sure you're including the ``--metadata`` option.

3. **Check Tokenizer Availability**: Some tokenizers might require additional dependencies.

4. **Consider File Encoding**: Non-standard file encodings might affect token counting accuracy.