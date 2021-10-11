# Ben Rombaut's Personal Website

[![deploy](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/gh_pages_deploy.yml)
[![bookshelf-syncer](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/sync_bookshelf.yml)
[![software-syncer](https://github.com/brombaut/benrombautca/actions/workflows/sync_software.yml/badge.svg)](https://github.com/brombaut/benrombautca/actions/workflows/sync_software.yml)

Source repository for my personal website. To check out the live version of the site, head over to [benrombaut.ca](https://www.benrombaut.ca).

## **Site Roadmap**

### **About Me**

Includes some basic info about myself, as well as 2 _timeline_ sections for my work and education.

### **Ben's Bookshelf**

Showcases books I've read and am currently reading. This is built using the [Goodreads API](https://www.goodreads.com/api) and an npm package I made called [F3 - Firebase Firestore Facade](https://www.npmjs.com/package/firebase-firestore-facade). I use Goodreads to keep track of books I've read, books I'm currently reading (includingwhat page I'm on), and books I want to read. I then mirror the data from Goodreads in my own Firebase Firestore database, which I keep synced using an instance of F3. Currently, this whole process sits in it's own repo (which I call _Bookshelf-Syncer_), with a GitHub action that triggers the syncing process multiple times throughout the day.

#### Future Work

- **✅ Merge Bookshelf-Syncer into this repo**  
  Right now, the code for syncing my bookshelf on Goodreads and my own cloud database is in another project. The plan is to move the code under this directory, and set up a GitHub Action cron for this repo to sync the two.

### **Articles**

A collection of how-to guides and notes I've written on different topics, mostly so that I can use them as references later. I originally write the articles using Markdown, and then translate the Markdown file to equivalent HTML files using [Pandoc](https://pandoc.org/). I then reference these source HTML files from my Articles section.

#### Future Work

- **Filter articles by tag**  
  As the number of articles grows, I'd like to be able to quickly find articles on specific topics. My initial plan for this feature is to filter by article tags.
- **Consider moving Article-Syncer to the cloud**  
  Right now, the code for syncing the Markdown files is in another repo (which I call _Article-Syncer_), and I have to manually run the script on my local machine to update the converted HTML files here. I'd like to actually have _Article-Syncer_ basically detect when I push a new Markdown article, run the Pandoc conversion, and store the resulting HTML source file in the cloud (e.g., an AWS S3 Bucket). Then I just have to keep track of a bit of Article meta-data on this repo. I still have to give this whole process a bit of thought though.

### **Software**

Showcases the README files of different software projects I've built. This process for showing these READMEs is very similar to the process for Articles (explained just above).

#### Future Work

- **✅ Merge Software-Syncer into this repo**  
  Right now, the code for syncing the READMEs from other software projects is in another repo (which I call _Software-Syncer_), and I have to manually run the script on my local machine to update the converted HTML README files here. The plan is to move the code under this directory, and set up a dispatchable GitHub Action that gets each projects README content from the GitHub repo, converts it to HTML, and syncs the version for this site.

### **General Future Work**

- **Migrate to Vue 3**  
  I'm currently using Vue 2, but it's on my radar to update all my dependencies, including moving to using Vue 3.
- **✅ Add Resume & CV PDFs**  
  Have the PDFs available in the external profiles section
