# Gemini Project: Personal Portfolio Website

## Project Overview

This project is a personal portfolio website for Ben Rombaut, a software developer. It is built using Vue 3 and TypeScript. The website showcases Ben's work experience, education, personal projects, publications, and hobbies.

The site is structured as a single-page application (SPA) using Vue Router for navigation. It features several sections:

*   **About Me:** A professional summary, work history, and education.
*   **Bookshelf:** A list of books read, synced from Goodreads.
*   **Articles:** A collection of technical articles written by Ben.
*   **Software:** A showcase of personal software projects.
*   **Publications:** A list of academic publications.
*   **Running & Hiking:** Photo galleries of outdoor activities.

The project uses SCSS for styling and Font Awesome for icons. It includes a series of scripts for syncing content from external sources like Goodreads and GitHub.

## Building and Running

The following commands are used to build and run the project:

*   **Install dependencies:**
    ```bash
    npm install
    ```
*   **Run the development server:**
    ```bash
    npm run serve
    ```
    The application will be available at `http://localhost:8080`.
*   **Build for production:**
    ```bash
    npm run build
    ```
    The production-ready files will be generated in the `dist/` directory.
*   **Run linter:**
    ```bash
    npm run lint
    ```
*   **Sync bookshelf:**
    ```bash
    npm run sync-bookshelf
    ```
*   **Sync articles:**
    ```bash
    npm run sync-articles
    ```

## Development Conventions

*   **Framework:** Vue 3 with the Composition API.
*   **Language:** TypeScript.
*   **Styling:** SCSS with a BEM-like methodology.
*   **Code Style:** The project uses ESLint with a configuration based on Airbnb's style guide. Key rules include:
    *   2-space indentation.
    *   Double quotes for strings.
*   **Commit Style:** The project uses Husky for pre-commit hooks.
*   **Testing:** There are no testing practices mentioned in the project.
