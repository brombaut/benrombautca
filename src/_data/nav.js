/*
 * Sidebar nav items and social links. Replaces FullNavBar.vue's hardcoded list
 * and the ExternalProfile class. `icon` names a file in src/_includes/icons/.
 */
module.exports = {
  items: [
    { label: "About", url: "/" },
    { label: "Bio", url: "/bio/" },
    { label: "Blog", url: "/blog/" },
    { label: "Publications", url: "/publications/" },
    { label: "Bookshelf", url: "/bookshelf/" },
    { label: "Running", url: "/running/" },
    { label: "Hiking", url: "/hiking/" },
  ],
  social: [
    { label: "GitHub", url: "https://github.com/brombaut", icon: "github" },
    { label: "LinkedIn", url: "https://www.linkedin.com/in/benjamin-rombaut/", icon: "linkedin" },
    { label: "Google Scholar", url: "https://scholar.google.ca/citations?user=hBX9eycAAAAJ&hl=en", icon: "google-scholar" },
  ],
};
