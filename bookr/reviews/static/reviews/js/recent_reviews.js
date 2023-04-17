const styles = {
    rowContent: {
        padding: "0px",
    },
    bookRow: {
        display: "flex",
        justifyContent: "space-between",
        flexDirection: "row",
        flexWrap: "wrap",
        rowGap: "10px",
        margin: "10px 0px"
    },
    article: {
        flex: "1",
    },
    bookCell: {
        boxSizing: "border-box",
        border: "thin solid #003554",
        backgroundColor: "white",
        padding: "10px",
        width: "300px",
        borderRadius: "10px"
    },
    btnSection: {
        display: "flex",
        justifyContent: "space-between",
        width: "100%",
    },
    btn: {
        backgroundColor: "#3ea7e4",
        color: "white",
    },
    "btn:disabled": {
        backgroundColor: "gray",
    },
    footer : {
        backgroundColor: "blue",
    }
};


class ReviewDisplay extends React.Component {
    constructor(props) {
        super(props);
        this.state = {review: props.review};
    }

    render() {
        // NOTE: Using JSX and React, "className" == "class" and gets
        // translated in HTML.
        const review = this.state.review;
        // Remember, we defined a user serializer.
        const creator = review.creator;

        return (
                <article style={ styles.bookCell } className="bookCell">
                    <section className="bookBody">
                        <h5 className="bookTitle">
                            { review.book } <strong>({ review.rating })</strong>
                        </h5>
                        <h6 className="creatorEmail">
                            { creator.email }
                        </h6>
                        <p className="reviewContent">{ review.content }</p>
                    </section>

                    <footer className="bookFooter">
                        <a href={"/books/" + review.book_id + "/"} className="card-link">
                            View Book
                        </a>
                    </footer>
                </article>);
    }
}


class RecentReviews extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            reviews: [],
            currentUrl: props.url,
            nextUrl: null,
            previousUrl: null,
            loading: false
        };
    }
    
    fetchReviews() {
        if (this.state.loading) {
            return;
        }

        this.setState({loading: true});
        fetch(
            this.state.currentUrl,
            {
                method: "GET",
                headers: {
                    Accept: "application/json"          
                }
            }
        ).then((response) => {
            // "response.json()" is used for a one-time read of the
            // response data stream.
            return response.json();
        }).then(
            (data) => {
                // The following keys in "data" are made available by
                // setting the "?limit" query on the 'api:review-list'
                // url in the HTML file.
                this.setState({
                    loading: false, reviews: data.results,
                    nextUrl: data.next, previousUrl: data.previous
                })
            }
        )
    }
    
    // NOTE: Method called when React has loaded a component onto the
    // page.
    componentDidMount() {
        this.fetchReviews();
    }

    loadNext() {
        if (this.state.nextUrl === null) {
            return;
        }
        this.setState({currentUrl: this.state.nextUrl});
        this.fetchReviews();
    }

    loadPrevious() {
        if (this.state.previousUrl === null) {
            return;
        }
        this.setState({currentUrl: this.state.previousUrl});
        this.fetchReviews();
    }

    render() {
        if (this.state.loading) {
            return <h5>Loading...</h5>;
        }
        
        // Button is disabled if the condition is true.
        const previousButton = (
            <button id="prevBtn" style={ styles.btn }
                onClick={ () => { this.loadPrevious() } }
                disabled={ this.state.previousUrl === null}>
                    Previous
            </button>);

        const nextButton = (
            <button id="nextBtn" style={ styles.btn }
                onClick={ () => { this.loadNext() } }
                disabled={ this.state.nextUrl === null }>
                    Next
            </button>);
        
        let reviewItems;
        // Note length method.
        if (this.state.reviews.length === 0) {
            reviewItems = <h5>No reviews to display.</h5>;
        }
        else {
            reviewItems = this.state.reviews.map((review) => {
                    // Using a component even inside here:
                    return <ReviewDisplay key={review.pk} review={review}/>;
            });
        }

        return (
            <section className="reviewContent" style={ styles.rowContent }>
                <section style={ styles.bookRow } className="book_row">
                    { reviewItems }
                </section>
                <section id="btnSection" style={ styles.btnSection }>
                    { previousButton }
                    { nextButton }
                </section>
            </section>
        );
    }
}
