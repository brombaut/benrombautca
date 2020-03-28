<template>
    <div class='book-card-in-progress'>
        <div
            v-if="imageSource"
            class='left-container'>
            <img :src='imageSource' />
        </div>
        <div class='right-container'>
            <div class='title'>{{ book.title }}</div>
            <div class='subtitle'>{{ book.subtitle }}</div>
            <p class='description'>{{ book.description }}</p>
            <div
                v-if="book.url"
                class='view-source-container'>
                <a :href="book.url">
                    <font-awesome-icon
                        @click.stop.prevent='handleSourceIconClick()'
                        :icon="['fas', 'code']" />
                </a>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'BookCardInProgress',
    props: {
        book: Object,
    },
    computed: {
        imageSource() {
            if (!this.book.thumbnail) {
                return '';
            }
            const images = require.context('../../assets/images/', false, /\.(jpg|png)$/);
            return images(`./${this.book.thumbnail}`);
        },
    },
    methods: {
        handleSourceIconClick() {
            if (!this.book.url) {
                return;
            }
            window.open(this.book.url, '_blank').focus();
        },
    },
};
</script>

<style lang='scss' scoped>

.book-card-in-progress {
    margin: 16px;
    display: flex;
    border: 1px solid $primaryDark;
    border-radius: 8px;
    width: 400px;
    height: 264px;
    background: $secondaryDark;

    .left-container {
        height: 100%;

        img {
            height: 100%;
            width: 200px;
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
        }
    }

    .right-container {
        display: flex;
        flex-direction: column;
        margin: 16px;

        .title {
            color: $primary;
            font-size: 20px;
        }

        .subtitle {
            color: $primaryDark;
        }

        .description {
            text-align: left;
            font-size: 14px;
        }

        .view-source-container {
            color: $primaryDark;
            display: flex;
            align-self: flex-end;
            justify-content: flex-end;
            margin-top: auto;
            font-size: 16px;
            transition: color 0.3s;

            a:visited {
                color: inherit;
            }

            &:hover {
                color: $primary;
            }
        }
    }
}

</style>
