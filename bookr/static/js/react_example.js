// Javascript + XML. Simplifies component creation.


class ClickCounter extends React.Component {
    constructor(props) {
        super(props);
        // Can read properties passed into the react component (as an
        // element) from the "props" object.
        this.state = {clickCount: 0, name: props.name, target: props.target};
    }

    // Each class-based component must have this method.
    render() {
        // Place javascript code in HTML sections in braces.
        if (this.state.clickCount == this.state.target) {
            return <span>Well done, {this.state.name}!</span>
        }
        // Using an arrow function is similar to using a lambda
        // function in Python.
        // Surround JS code within an HTML section with braces.
        return <button onClick={
            () => this.setState(
                {clickCount: this.state.clickCount + 1}
            )
        }>
            {this.state.clickCount}
        </button>;
    }
}


// Can now treat the component as an element.
// Commented out since we've moved it to the HTML template.
// ReactDOM.render(<ClickCounter/>, document.getElementById("react_container"));


class BookDisplay extends React.Component {
    constructor(props) {
        super(props);
        this.state = {books: [], url: props.url, fetchInProgress: false}
    }

    doFetch() {
        if (this.state.fetchInProgress) {
            return;  // Return "null."
        }
        
        this.setState({fetchInProgress: true});
        // Fetch returns a JS promise. The "json()" method on a
        // response also returns a promise, and we can chain such
        // calls as shown. (A promise takes a callback function
        // that takes an async function's return value as an arg.)
        fetch(this.state.url,
            {
                method: "GET",
                headers: {
                    // Header keys are case insensitive, though.
                    Accept: "application/json"
                }
            }
        ).then((response) => {
            return response.json();
        }).then((data) => {
            this.setState({fetchInProgress: false, books: data});
        });
    }

    render() {
        // Equiv to "dict.map(lambda book: ...)."
        // "this.state.books" and "book" are "objects."
        // (Check what the django API returns in "".../api/books" to
        // confirm.)
        const bookListItems = this.state.books.map(
            // Result is an array with HTML elements.
            (book) => {
                // Must have a key for each element in the HTML list.
                // RESEARCH: Why does "book.pk" work if the API doesn't
                // return "pk for books"
                return <li key={ book.pk }>{ book.title }</li>;
            }
        )
        
        // Cond ? <exec if cond True>: <exec if False>.
        const buttonText = this.state.fetchInProgress ? "Fetch in Progress" : "Fetch";

        return <div>
            <ul>{ bookListItems }</ul>
            <button onClick={ () => this.doFetch() }
                disabled={ this.state.fetchInProgress }>
                    { buttonText }
            </button>
        </div>;
    }
}