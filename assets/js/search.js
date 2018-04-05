import React from 'react';
import ReactDOM from 'react-dom';
import 'whatwg-fetch';
import {constructImagePath, WineList} from "./shared";

const queryString = require('query-string');

// todo: figure out how to django-ize these
const SEARCH_API_URL = '/api/search/';


class SearchByNameControl extends React.Component {
    render () {
        return (
            <div>
                <label htmlFor="search">Search: </label>
                <input type="text" id="search" placeholder="Warwick" value={this.props.searchText}
                       onChange={(e) => this.props.searchTextChanged(e.target.value)}/>
                <button onClick={() => this.props.doSearch()}>Search</button>
            </div>
        );
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
        return (
            <div className="container">
                <SearchByNameControl searchText={this.state.searchText}
                                     searchTextChanged={(text) => this.searchTextChanged(text)}
                                     doSearch={() => this.doSearch()}
                />
                <WineList wines={this.state.wines} isLoading={this.state.isLoading}/>
            </div>
        )
    }

    searchTextChanged(text) {
        this.setState({
            searchText: text
        });
    }

    doSearch() {
        let params = queryString.stringify({q: this.state.searchText});
        fetch(SEARCH_API_URL + '?' + params).then((response) => this._updateResultsFromResponse(response));
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
}

ReactDOM.render(
    <SearchByNamePage/>,
    document.getElementById('react-home')
);
