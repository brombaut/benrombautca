<template>
    <div class='project-card'>
        <div class='upper-container'>
            <div class='name'>
                {{ project.name }}
            </div>
            <div class='description'>
                {{ project.description }}
            </div>
        </div>

        <div class='lower-container'>
            <div class='tech-used'>
                <h5>Tech Used</h5>
                <ul>
                    <li
                        v-for="tech in project.techUsed"
                        :key="tech">
                        {{ tech }}
                    </li>
                </ul>
            </div>
            <div class='thumbnail-container'>
                <img :src='imageSource' />
            </div>
        </div>

    </div>
</template>

<script>
export default {
    name: 'ProjectCard',
    props: {
        project: Object,
    },
    computed: {
        imageSource() {
            const images = require.context('../../assets/images/', false, /\.png$/);
            return images(`./${this.project.thumbnail}`);
        },
    },
};
</script>

<style lang='scss'>
.project-card {
    width: 550px;
    min-height: 380px;
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

    @keyframes borderColorChange {
        0% {
            border-color: $primaryPulse1;
        }
        25% {
            border-color: $primaryPulse2;
        }
        50% {
            border-color: $primaryPulse3;
        }
        75% {
            border-color: $primaryPulse4;
        }
        100% {
            border-color: $primaryPulse1;
        }
    }
}
</style>
