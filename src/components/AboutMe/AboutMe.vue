<template>
    <div id='about-me'>
        <h1>About Me</h1>
        <div class='content-container'>
            <div class='paragraphs-container'>
                <p
                    v-for="obj in aboutMe.description"
                    :key="obj.section">
                    {{ obj.paragraph }}
                </p>
            </div>
            <div class='image-container'>
                <img :src='imageSource' />
            </div>
        </div>
        <div class='footer'></div>
    </div>
</template>

<script>
import aboutMe from '@/data/aboutMe';

export default {
    name: 'AboutMe',
    data() {
        return {
            aboutMe,
        };
    },
    computed: {
        imageSource() {
            if (!this.aboutMe.imageFileName) {
                return '';
            }
            const images = require.context('../../assets/images/', false, /\.jpg$/);
            return images(`./${this.aboutMe.imageFileName}`);
        },
    },
};
</script>

<style lang='scss'>
#about-me {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    overflow-x: auto;

    .content-container {
        background: $secondaryLight;
        width: 1000px;
        padding: 8px 16px;
        border-radius: 8px;;
        border: 1px solid $primaryDark;
        animation: borderColorChange $pulseAnimationTime infinite;
        display: flex;
        align-items: center;

        .paragraphs-container {
            flex: 1;
            p {
                text-align: left;
                color: white;
                font-size: 20px;
            }
        }

        .image-container {
            height: 300px;
            width: 300px;
            border: 2px solid $primaryDark;
            animation: borderColorChange $pulseAnimationTime infinite;
            border-radius: 50%;
            margin: 0 9px;

            img {
                height: 100%;
                width: 100%;
                border-radius: 50%;;
            }
        }
    }

    .footer {
        height: 120px;
    }

}

</style>
