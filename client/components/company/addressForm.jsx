import React, { Component } from 'react';

const addressConfig = [
    {id:'address', name: 'address', placeholder: 'Address'},
    {id:'ste', name: 'ste', placeholder: 'Ste or Apt'},
    {id:'city', name: 'city', placeholder: 'City'},
]

class AddressForm extends Component{
    state = {
        addressType: '',
        address:'',
        ste:'',
        city:'',
        state:'',
        zip:''
    }
    render(){
        return(
            <div className="row">
            <div className="col-12 col-sm-6">
                    <label htmlFor="addressType">Address Type</label><br/>
                    <select
                        id="addressType" 
                        className="form-control"
                        name="addressType"
                        value={status|| ""}
                        onChange={this.handleChange}
                        required
                    >
                        <option value="">--Select--</option>
                        <option value="billing">billing</option>
                        <option value="building">building</option>
                        <option value="residential">residential</option>
                        <option value="office">office</option>
                    </select>
            </div>
            {
                addressConfig.map(({id, name, placeholder}) => {
                    return(
                        <div className="col-12 col-sm-6">
                        <label htmlFor={name}>{placeholder}</label>
                        <input 
                            id={id}
                            className="form-control"
                            name={name}
                            value={''}
                            placeholder={placeholder}
                        />
                        </div>
                    )
                   
                })
            }
             <div className="col-12 col-sm-6">
                    <label htmlFor="addressType">Address Type</label><br/>
                    <select
                        id="addressType" 
                        className="form-control"
                        name="addressType"
                        value={status|| ""}
                        onChange={this.handleChange}
                        required
                    >
                        <option value="">--Select--</option>
                        <option value="billing">billing</option>
                        <option value="building">building</option>
                        <option value="residential">residential</option>
                        <option value="office">office</option>
                    </select>
            </div>
            <div className="col-12 col-sm-6">
                    <label htmlFor="zip">Zip</label><br/>
                    <input 
                            id="zip"
                            className="form-control"
                            name="zip"
                            value={this.state.zip}
                            placeholder={"Zip"}
                        />
                        </div>
                        <div className="col-12 col-sm-6">
                    <div className="form-check">
                        <input id="default-address" className="form-check-input" name="default-address" type="checkbox"/>
                        <label id="default-address" htmlFor="default-address">Default</label>
                    </div>
                </div>
            </div>

        )
    }
}

export default AddressForm;