import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';
import {WineList, Paginator} from "./shared";

const queryString = require('query-string');

// todo: figure out how to django-ize these
const SEARCH_API_URL = '/api/search/';


class SearchByNameControl extends React.Component {
    render () {
        return (
            <div>
                <label htmlFor="search">Search: </label>
                <input type="text" id="search" placeholder="Warwick" value={this.props.searchText}
                       onChange={(e) => this.props.searchTextChanged(e.target.value)}
                       onKeyPress={(e) => this.handleKeyPress(e.key)}
                />
                <button onClick={() => this.props.doSearch()}>Search</button>
            </div>
        );
    }

    handleKeyPress(key) {
        if (key === 'Enter') {
            this.props.doSearch();
        } else {
            console.log('not enter', key);
        }
    }
}

class SearchResults extends React.Component {
    render () {
        return (
            <ul>
                <li>todo</li>
                <li>todo</li>
                <li>todo</li>
            </ul>
        )
    }
}

class SearchByNamePage extends React.Component {
    constructor() {
        super();
        this.state = {
            searchText: '',
            // results / pagination
            wines: [],
            resultCount: 0,
            resultPage: 1,
            resultStart: 1,
            resultEnd: 10,
            nextPageUrl: null,
            prevPageUrl: null,
            firstSearchMade: false,
            isLoading: false,
        }
    }

    render() {
        let showPaginator = (this.state.wines.length);
        let paginator = showPaginator ? <Paginator
            nextPage={() => this.nextPage()} showNext={Boolean(this.state.nextPageUrl)}
            prevPage={() => this.prevPage()} showPrevious={Boolean(this.state.prevPageUrl)}
            count={this.state.resultCount} page={this.state.resultPage}
            start={this.state.resultStart} end={this.state.resultEnd}
        /> : '';

        return (
            <div className="container">
                <SearchByNameControl searchText={this.state.searchText}
                                     searchTextChanged={(text) => this.searchTextChanged(text)}
                                     doSearch={() => this.doSearch()}
                />
                <WineList wines={this.state.wines} isLoading={this.state.isLoading}/>
                {paginator}
            </div>
        )
    }

    componentDidMount() {
        let queryParams = queryString.parse(location.search);
        if (Object.keys(queryParams).length && queryParams['q']) {
            this.setState({
                searchText: queryParams['q']
            }, this.doSearch);
        }
    }

    searchTextChanged(text) {
        this.setState({
            searchText: text
        });
    }

    doSearch() {
        let params = queryString.stringify({q: this.state.searchText});
        fetch(SEARCH_API_URL + '?' + params).then((response) => this._updateResultsFromResponse(response));
        window.history.replaceState(params, 'Search Results', `/search-by-name/?${params}`)
    }

    _updateResultsFromResponse(response) {
        if (response.ok) {
            response.json().then((responseJson) => {
                console.log(responseJson);
                this.setState({
                    wines: responseJson.results,
                    nextPageUrl: responseJson.next,
                    prevPageUrl: responseJson.previous,
                    resultCount: responseJson.count,
                    resultPage: responseJson.page,
                    resultStart: responseJson.start,
                    resultEnd: responseJson.end,
                    isLoading: false,
                });
            });
        }
    }

    nextPage() {
        if (this.state['nextPageUrl']) {
            fetch(this.state['nextPageUrl']).then((response) => this._updateResultsFromResponse(response));
        }
    }

    prevPage() {
        if (this.state['prevPageUrl']) {
            fetch(this.state['prevPageUrl']).then((response) => this._updateResultsFromResponse(response));
        }
    }

}

ReactDOM.render(
    <SearchByNamePage/>,
    document.getElementById('react-home')
);
