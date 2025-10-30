# Integrate MCP with GitHub Copilot

_Learn how to give GitHub Copilot more tools to expand the capabilities of your development workflow. All in less than an hour!_

## Welcome

- **Who is this for**: Developers looking to enhance their AI-assisted workflows, GitHub Copilot users, and AI enthusiasts.
- **What you'll learn**: We'll introduce MCP basics, a GitHub MCP server setup, and integration with Copilot Agent Mode.
- **What you'll build**: A mixed development workflow that uses GitHub Copilot to manage issues while upgrading the extracurricular activities website for Mergington High School.
- **Prerequisites**: [Getting Started with Copilot](https://github.com/skills/getting-started-with-github-copilot) Exercise
- **How long**: This exercise takes less than one hour to complete.

In this exercise, you will:

1. Integrate a GitHub MCP server with GitHub Copilot.
2. Delegate Copilot to research similar projects and open issues.
3. Ask Copilot to find an important issue and implement it from idea to pull request.
4. Add comments to a recently closed issue.

### How to start this exercise

> [!IMPORTANT]
> This exercise assumes basic knowledge of [GitHub Copilot](https://github.com/features/copilot). If you are unfamiliar, we recommend the [Getting Started with Copilot](https://github.com/skills/getting-started-with-github-copilot) exercise.

Simply copy the exercise to your account, then give your favorite Octocat (Mona) **about 20 seconds** to prepare the first lesson, then **refresh the page**.

[![](https://img.shields.io/badge/Copy%20Exercise-%E2%86%92-1f883d?style=for-the-badge&logo=github&labelColor=197935)](https://github.com/new?template_owner=skills&template_name=integrate-mcp-with-copilot&owner=%40me&name=skills-integrate-mcp-with-copilot&description=Exercise:+Integrate+Model+Context+Protocol+with+GitHub+Copilot&visibility=public)

<details>
<summary>Having trouble? 🤷</summary><br/>

When copying the exercise, we recommend the following settings:

- For owner, choose your personal account or an organization to host the repository.

- We recommend creating a public repository, since private repositories will use Actions minutes.

If the exercise isn't ready in 20 seconds, please check the [Actions](../../actions) tab.

- Check to see if a job is running. Sometimes it simply takes a bit longer.

- If the page shows a failed job, please submit an issue. Nice, you found a bug! 🐛

</details>

## The Mergington High School Activities Application

This exercise includes a sample FastAPI application for managing extracurricular activities at Mergington High School. The application allows students to view available activities and sign up for them.

### Quick Start

To run the application locally:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   cd src
   uvicorn app:app --reload
   ```

3. **Access the application**:
   - Web interface: http://localhost:8000
   - API documentation (Swagger UI): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

For detailed information about the API, features, and usage examples, see the [Application README](src/README.md).

### Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to get started.

### Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) for details.

---

&copy; 2025 GitHub &bull; [Code of Conduct](CODE_OF_CONDUCT.md) &bull; [MIT License](https://gh.io/mit)
