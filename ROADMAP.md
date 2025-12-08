# Strategic ROADMAP.md

> **Goal**: Balance Innovation, Stability, and Debt.
> **Status**: Living Document (V3.0)

---

## 🏁 Phase 0: The Core (Stability & Debt)
**Goal**: Solid foundation. Build a codebase that is easy to maintain and contribute to.

- [ ] **Testing**: Coverage > 95% (Current: ~97%). `[Feat]` `[S]`
- [ ] **CI/CD**: Linting, Type Checking (mypy), Pre-commit hooks. `[Debt]` `[S]`
- [ ] **Documentation**: Comprehensive README with clear usage examples. `[Feat]` `[M]`
- [ ] **Refactoring**: Pay down critical technical debt (unused imports, variables). `[Debt]` `[S]`

---

## 🚀 Phase 1: The Standard (Feature Parity)
**Goal**: Competitiveness. Ensure `pyinitgen` has all the features expected of a modern CLI tool.
*Requires Phase 0*

- [ ] **UX**: CLI improvements, rich error messages, progress bars. `[Feat]` `[M]`
- [ ] **Config**: Robust settings management via `pyproject.toml` and `.pyinitgen.toml`. `[Feat]` `[M]`
- [ ] **Performance**: optimize recursive scanning for large codebases. `[Feat]` `[L]`
- [ ] **Watch Mode**: Automatically create `__init__.py` files as directories are created. `[Feat]` `[L]`
- [ ] **Interactive Mode**: Prompt user before creating files. `[Feat]` `[M]`
- [ ] **Detailed Reporting**: Generate reports of created files. `[Feat]` `[M]`

---

## 🔌 Phase 2: The Ecosystem (Integration)
**Goal**: Interoperability. Make `pyinitgen` play well with others.
*Requires Phase 1*

- [ ] **API**: Expose core logic as a library (REST/GraphQL if applicable, or just clean Python API). `[Feat]` `[L]`
- [ ] **Plugins**: Extension system (e.g., adding `__all__` automatically). `[Feat]` `[XL]`
- [ ] **IDE Integration**: VS Code / PyCharm plugins. `[Feat]` `[XL]`
- [ ] **GitHub Action**: Official action for CI pipelines. `[Feat]` `[M]`
- [ ] **Pre-commit Hook**: Official hook for `pre-commit`. `[Feat]` `[S]`

---

## 🔮 Phase 3: The Vision (Innovation)
**Goal**: Market Leader. Features that define the next generation of tooling.
*Requires Phase 2*

- [ ] **AI**: LLM Integration for generating `__init__.py` content. `[Feat]` `[XXL]`
- [ ] **Cloud**: K8s/Docker integrations if applicable. `[Feat]` `[L]`
- [ ] **Graph Analysis**: Analyze import graphs to fix circular dependencies. `[Feat]` `[XL]`
- [ ] **Cross-Language**: Support for other languages with similar module systems. `[Feat]` `[XXL]`

---

## Legend
- `[Debt]`: Technical Debt / Maintenance
- `[Feat]`: New Feature
- `[Bug]`: Bug Fix
- `[S/M/L/XL]`: T-Shirt Size Estimate
