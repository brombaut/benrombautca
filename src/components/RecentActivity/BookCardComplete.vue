<template>
    <div class='book-card-complete'>
        <div
            v-if="imageSource"
            class='image-container'>
            <img :src="imageSource" />
        </div>
        <div class='book-info'>
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
    name: 'BookCardComplete',
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
.book-card-complete {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0 32px;
    min-width: 200px;
    border: 1px solid $primaryDark;
    border-radius: 8px;
    background: $secondaryDark;
    padding: 16px 8px;
    height: fit-content;

    .image-container {
        height: 164px;
        width: 120px;

        img {
            width: 100%;
            height: 100%;
        }
    }

    .book-info {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 4px;

        .title {
            color: $primary;
            font-size: 16px;
        }

        .subtitle {
            color: $primaryDark;
            font-size: 14px;
        }

        .description {
            text-align: left;
            font-size: 11px;
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
