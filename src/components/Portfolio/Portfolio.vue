<template>
    <div id='portfolio'>
        <h1>Projects</h1>
        <div class='project-card-container'>
            <ProjectCard
                v-for="project in projects"
                :key="project.id"
                :project="project" />
        </div>
    </div>
</template>

<script>
import ProjectCard from '@/components/Portfolio/ProjectCard.vue';

export default {
    name: 'Portfolio',
    components: {
        ProjectCard,
    },
    data() {
        const projects = [
            {
                id: 1,
                name: 'BEC Article Tracker',
                description: 'A simple tool I use to keep track of tech-related articles I have read and articles I would like to read.',
                techUsed: [
                    'Vue,js',
                    'Firebase',
                ],
                link: 'https://brombaut.github.io/article-tracker/',
                sourceLink: 'https://github.com/brombaut/article-tracker',
                thumbnail: 'BecArticleTracker.png',
                inProgress: false,
            },
            {
                id: 2,
                name: 'Stack Overflow Question Scraper',
                description: 'A site that allows users to quickly build queries for questions on Stack Overflow, view summaries of these questions, and quickly view the full question on Stack Overflow.',
                techUsed: [
                    'Vue,js',
                    'Cheerio',
                ],
                link: 'https://brombaut.github.io/stack-overflow-question-scraper/',
                sourceLink: 'https://github.com/brombaut/stack-overflow-question-scraper',
                thumbnail: 'StackOverflowQuestionScraper.png',
                inProgress: false,
            },
        ];
        return {
            projects,
        };
    },
};
</script>

<style lang='scss'>
#portfolio {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;

    h1 {
        margin-top: 32px;
    }

    .project-card-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }
}

</style>
