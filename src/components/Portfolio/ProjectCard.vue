<template>
    <a
        class='project-card'
        :href="project.url || project.sourceUrl"
        @click.prevent='handleProjectCardClick()'>
        <div class='upper-container'>
            <div class='name'>
                {{ project.name }}
            </div>
            <div class='description'>
                {{ project.description }}
            </div>
        </div>

        <div class='lower-container'>
            <div
                v-if="project.inProgress"
                class='in-progress'>
                Work In Progress...
            </div>
            <div
                v-else
                class='left-lower-container'>
                <div
                    v-if="project.techUsed"
                    class='tech-used'>
                    <h5>Tech Used</h5>
                    <ul>
                        <li
                            v-for="tech in project.techUsed"
                            :key="tech">
                            {{ tech }}
                        </li>
                    </ul>
                </div>
                <div class='view-source-container'>
                    <a :href="project.sourceUrl">
                        <font-awesome-icon
                            @click.stop.prevent='handleSourceIconClick()'
                            :icon="['fas', 'code']" />
                    </a>
                </div>
            </div>
            <div
                v-if="imageSource"
                class='thumbnail-container'>
                <img :src='imageSource' />
            </div>
        </div>
    </a>
</template>

<script>
export default {
    name: 'ProjectCard',
    props: {
        project: Object,
    },
    computed: {
        imageSource() {
            if (!this.project.thumbnail) {
                return '';
            }
            const images = require.context('../../assets/images/', false, /\.png$/);
            return images(`./${this.project.thumbnail}`);
        },
    },
    methods: {
        handleProjectCardClick() {
            const url = this.project.url ? this.project.url : this.project.sourceUrl;
            if (url) {
                window.open(this.project.url, '_blank').focus();
            }
        },
        handleSourceIconClick() {
            if (!this.project.sourceUrl) {
                return;
            }
            window.open(this.project.sourceUrl, '_blank').focus();
        },
    },
};
</script>

<style lang='scss'>
.project-card {
    text-decoration: none;
    width: 550px;
    min-height: 200px;
    background: $secondaryLight;
    border: 1px solid $primaryDark;
    margin: 40px;
    box-shadow: 5px 5px 5px $secondaryDark;
    transition: transform 0.3s;
    animation: borderColorChange $pulseAnimationTime infinite;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .upper-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 8px;

        .name {
            padding: 12px;
            color: $primary;
            font-size: 28px;
        }

        .description {
            padding: 4px 16px;
            text-align: left;
            color: white;
        }
    }

    .lower-container {
        display: flex;
        justify-content: space-between;

        .in-progress {
            margin: 40px 0;
            padding: 8px 0px;
            width: 100%;
            color: white;
            background: $primaryDark;
        }

        .left-lower-container {
            display: flex;
            flex-direction: column;
            justify-content: space-between;

            .tech-used {
                color: white;
                padding-left: 16px;

                h5 {
                    color: $primaryDark;
                    margin: 0;
                    font-size: 20px;
                }

                ul {
                    list-style-type: none;
                    margin: 0;
                    padding: 0;

                    li {
                        padding: 8px;
                        text-align: left;
                    }
                }
            }

            .view-source-container {
                color: $primaryDark;
                display: flex;
                justify-content: flex-start;
                margin: 8px 16px;
                font-size: 24px;
                transition: color 0.3s;

                a:visited {
                    color: inherit;
                }

                &:hover {
                    color: $primary;
                }
            }
        }

        .thumbnail-container {
            height: 225px;
            width: 400px;
            background: $secondaryLightest;

            img {
                height: 100%;
                width: 100%;
            }
        }
    }

    &:hover {
        transform: scale(1.03);
        cursor: pointer;
    }
}
</style>
