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
import projects from '@/data/projects';

export default {
    name: 'Portfolio',
    components: {
        ProjectCard,
    },
    data() {
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
    overflow-x: auto;

    .project-card-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
    }
}

</style>
