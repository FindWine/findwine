import React from 'react';
import ReactDOM from 'react-dom';


class SearchControls extends React.Component {

  render() {
    return (
      <div>
      <h5 style={{paddingTop: '10%', paddingBottom: '5%', textAlign: 'center'}}>What wine would you like to find?</h5>
  		<form className="search-form" role="search" action="/search/" method="get">
  			<div className="row d-flex align-items-end">
  				<div className="col-sm-3">
  					<div className="form-group category">
  						<label htmlFor="id_category">Category</label>
  						<select name="category" id="id_category">
    <option value="Red" selected>Red</option>

    <option value="White">White</option>

    <option value="Rosé">Rosé</option>

    <option value="Bubbly">Bubbly</option>

    <option value="Dessert Wine">Dessert Wine</option>

    <option value="Port">Port</option>

    <option value="Brandy/Husk Spirit">Brandy/Husk Spirit</option>

  </select>

  					</div>
  				</div>
  				<div className="col-sm-3">
  					<div className="form-group sub_category">
  						<label htmlFor="id_sub_category">Type</label>
  						<select name="sub_category" id="id_sub_category">
              </select>
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<div className="form-group min_price">
  						<label htmlFor="id_min_price">Minimum Price</label>
  						<input className="form-control" type="number" name="min_price" value="0" min="0" required id="id_min_price" />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<div className="form-group max_price">
  						<label htmlFor="id_max_price">Maximum Price</label>
  						<input className="form-control" type="number" name="max_price" value="500" min="0" required id="id_max_price" />
  					</div>
  				</div>
  				<div className="col-sm-2">
  					<button type="submit" className="btn btn-primary btn-block" style={{marginBottom: '16px', marginTop: '16px'}}>Find wine</button>
  				</div>
  			</div>
  		</form>
  	</div>
    )
  }
}
class SearchPage extends React.Component {
  // constructor() {
  // }

  render() {
    return (
      <div className="container">
        <SearchControls />
      </div>
    )
  }
}

ReactDOM.render(

  <SearchPage />,
  document.getElementById('react-home')
);
