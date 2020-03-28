<template>
    <div class='book-completed-container'>
        <div class='book-image-container'>
            <BookCardComplete
                v-for="book in books"
                :key="book.id"
                :book="book" />
        </div>
    </div>
</template>

<script>
import BookCardComplete from '@/components/RecentActivity/BookCardComplete.vue';

export default {
    name: 'BookCompletedContainer',
    props: {
        books: Array,
    },
    components: {
        BookCardComplete,
    },
};
</script>

<style lang='scss'>
.book-completed-container {
    width: 100%;

    .book-image-container {
        display: flex;
        overflow-x: auto;
        padding: 32px 0;
    }
}

</style>
