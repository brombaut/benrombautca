<template>
    <div id='portfolio'>
        <div class='scroll-container'>
            <h1>Projects</h1>
            <div class='project-card-container'>
                <ProjectCard
                    v-for="project in projects"
                    :key="project.id"
                    :project="project" />
            </div>
        </div>
        <ConnectorElementSingleUpward />
        <ConnectorElementDouble />
    </div>
</template>

<script>
import ProjectCard from '@/components/Portfolio/ProjectCard.vue';
import ConnectorElementSingleUpward from '@/components/Portfolio/ConnectorElementSingleUpward.vue';
import ConnectorElementDouble from '@/components/Portfolio/ConnectorElementDouble.vue';
import projects from '@/data/projects';

export default {
    name: 'Portfolio',
    components: {
        ProjectCard,
        ConnectorElementSingleUpward,
        ConnectorElementDouble,
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
    position: relative;

    .scroll-container {
        z-index: 1;
        overflow-x: auto;

        .project-card-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }

    }
}

</style>
