# Contributing to SME Valuation MCP

Thank you for your interest in contributing! This project welcomes PRs, bug reports, and feature suggestions from the community.

---

## Ways to Contribute

- **Bug reports** — open an issue with steps to reproduce and expected vs actual output
- - **Feature requests** — open an issue describing the use case and proposed solution
  - - **Code contributions** — fork the repo, make your changes, open a PR
    - - **Documentation** — improve README, add examples, fix typos
     
      - ---

      ## Getting Started

      ```bash
      # Fork and clone
      git clone https://github.com/<your-username>/sme-valuation-mcp.git
      cd sme-valuation-mcp

      # Install dependencies
      python -m venv .venv && .venv\Scripts\activate
      pip install -r requirements.txt

      # Run tests to verify everything works
      python -m unittest discover -s tests -p "test_*.py" -v
      ```

      ---

      ## Good First Issues

      Look for issues tagged [`good first issue`](../../issues?q=label%3A%22good+first+issue%22) — these are well-scoped tasks ideal for first-time contributors.

      ---

      ## Pull Request Guidelines

      1. **Fork** the repository and create a branch from `main`
      2. 2. **Write or update tests** for any logic you change
         3. 3. **Run the full test suite** before submitting: `python -m unittest discover -s tests -p "test_*.py" -v`
            4. 4. **Keep PRs focused** — one feature or fix per PR
               5. 5. **Write a clear PR description** explaining what changed and why
                 
                  6. ---
                 
                  7. ## Areas Where Help Is Most Needed
                 
                  8. | Area | Description |
                  9. |------|-------------|
                  10. | Valuation methods | Add new methods (e.g. LBO, NAV, transaction multiples) |
                  11. | Sector databases | Add sector-specific EV/EBITDA multiple ranges |
                  12. | Multi-currency | Support non-EUR/USD base currencies |
                  13. | LangChain adapter | Wrap MCP tools as LangChain tools |
                  14. | Test coverage | Expand unit and integration test coverage |
                  15. | Documentation | Examples for specific industries or scenarios |
                 
                  16. ---
                 
                  17. ## Code Style
                 
                  18. - Follow PEP 8
                      - - Use type hints where practical
                        - - Keep functions small and single-purpose
                          - - Add docstrings to public functions
                           
                            - ---

                            ## Reporting Bugs

                            Please include:
                            - Python version and OS
                            - - Steps to reproduce
                              - - Input payload (anonymize if needed)
                                - - Actual output vs expected output
                                 
                                  - ---

                                  ## License

                                  By contributing, you agree that your contributions will be licensed under the MIT License.
