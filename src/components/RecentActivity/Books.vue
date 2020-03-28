<template>
    <div id='books'>
        <h3>Books</h3>
        <div id='in-progress-container'>
            <h6>What I'm currently reading...</h6>
            <div class='book-card-container'>
                <BookCardInProgress
                    v-for="book in inProgressBooks"
                    :key="book.id"
                    :book="book" />
            </div>
        </div>
        <div id='completed-container'>
            <h6>What I've read...</h6>
            <BookCompletedContainer :books="completedBooks" />
            <!-- <div
                v-for="book in completedBooks"
                :key="book.id"
                class='in-progress-book-card'>
                {{ book.title }}
            </div> -->
        </div>
    </div>
</template>

<script>
import BookCardInProgress from '@/components/RecentActivity/BookCardInProgress.vue';
import BookCompletedContainer from '@/components/RecentActivity/BookCompletedContainer.vue';
import books from '@/data/books';

export default {
    name: 'Books',
    data() {
        return {
            books,
        };
    },
    components: {
        BookCardInProgress,
        BookCompletedContainer,
    },
    computed: {
        inProgressBooks() {
            return this.books.filter(book => book.inProgress);
        },
        completedBooks() {
            return this.books
                .filter(book => !book.inProgress)
                .sort((a, b) => a.id > b.id ? -1 : 1);
        },
    },
};
</script>

<style lang='scss'>
#books {
    background: $secondaryLight;
    width: 1200px;
    padding: 8px 16px;
    border-radius: 8px;;
    border: 1px solid $primaryDark;
    animation: borderColorChange $pulseAnimationTime infinite;
    display: flex;
    flex-direction: column;
    align-items: center;
    color: white;
    margin-bottom: 24px;
    box-shadow: 5px 5px 5px $secondaryDark;

    h3 {
        padding: 12px;
        color: $primary;
        font-size: 28px;
        margin: 0;
    }

    h6 {
        margin: 0 40px;
        color: $primaryDark;
        font-size: 20px;
    }

    #in-progress-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        width: 100%;

        .book-card-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
    }

    #completed-container {
        flex: 1;
        padding: 8px 0px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
}

</style>
