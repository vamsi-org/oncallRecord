'use strict';

const e = React.createElement;

class Dashboard extends React.Component {

  render() {

    return e(
      'h1',
      {},
      'Hello world!'
    );
  }
}

const domContainer = document.querySelector('#dashboard');
ReactDOM.render(e(Dashboard), domContainer);