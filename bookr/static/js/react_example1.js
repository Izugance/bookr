const e = React.createElement;  // Aliasing for ease.


// Class-based component.
class ClickCounter extends React.Component {
    // "props" is an object (dict-like, but js) passed between
    // components. Can contain data and attrs the element should have.
    constructor(props) {
        super(props);
        /* "this" is implicit, and is similar to "self."
        
        Each component has the "state" attribute which should be set
        with the "setState" method.
        
        This dict-like thing is called an "object." YOu don't need to
        put quotes around its keys. */
        this.state = {clickCount: 0};
    }

    // Each class-based component must have this method.
    render() {
        return e(
            "button",  // Element's name.
            // Using an arrow function to define the "onClick" attr.
            // Arrow functions retain the context of "this."
            {onClick: () => this.setState(
                {clickCount: this.state.clickCount + 1}
            )},
            this.state.clickCount  // Element's content.
        );
    }
}


/* Dump component in HTML "div" with given id.
Syntax: ReactDOM.render(component_element, container). 

Note that you don't have to put a ";" at the end of every js line. */
ReactDOM.render(e(ClickCounter), document.getElementById("react_container"))
