import React, { Component, Fragment } from 'react';
import AddressForm from './addressForm';
import CSRFToken from '../csrfToken';
const fieldConfig = [
    { id: 'name', name: 'name', placeholder: 'Name', required: true, type: 'text'},
    { id: 'phone', name: 'phone', placeholder: 'Phone', required: true, type: 'text'},
    { id: 'fax', name: 'fax', placeholder: 'Fax', required: true, type: 'text'},
    { id: 'email', name: 'email', placeholder: 'Email', required: true, type: 'email'},
    { id: 'website', name: 'website', placeholder: 'Website', required: true, type: 'url'},
    { id: 'facebook', name: 'facebook', placeholder: 'Facebook Link', required: true, type: 'url'},
    { id: 'twitter', name: 'twitter', placeholder: 'Twitter Link', required: true, type: 'url'},
    { id: 'linkedin', name: 'linkedin', placeholder: 'Linkedin Link', required: true, type: 'url'},
    { id: 'instagram', name: 'instagram', placeholder: 'Instagram Link', required: true, type: 'url'},
    { id: 'youtube', name: 'youtube', placeholder: 'Youtube', required: true, type: 'url'},
,
]

class CompanyForm extends Component {
        state = {
            name: '',
            phone: '',
            fax: '',
            email: '',
            website: '',
            facebook: '',
            twitter: '',
            linkedin: '',
            instagram: '',
            youtube:'',
            timezone: '',
            status: '',
            addresses: ["842688fe-c610-4fc3-952a-4f85f84ec4cd"],
            timezones: [],
            displaySecond: false,
            csrfmiddlewaretoken: ''
        }
    componentDidMount(){
        fetch('/api/core/timezone')
            .then(result => result.json())
            .then(data => {
                this.setState({timezones: data.results})
            })
    };

    handleChange = (e)  => {
        this.setState({
            [e.target.name]: e.target.value
        })
    }

    setToken = (token) => {
        this.setState({ csrfmiddlewaretoken: token })
    }
    handleSubmit = (e) => {
        e.preventDefault();
        const { timezones, displaySecond, ...submissionValues } = this.state;
        console.log(submissionValues);
        let formData = new FormData();
        Object.entries(this.state).forEach(item => {
            if(item[0] !== ("csrfmiddlewaretoken" || "displaySecond" || "timezones") ) {
                formData.append(item[0], item[1]);  
            }
        })
        fetch('/api/core/company/', {
            headers: {
                'X-CSRFToken': this.state.csrfmiddlewaretoken
            },
            method: 'POST',
            body: formData,
            credentials: 'same-origin',
        })
    }
    render(){
        const { timezone, status, timezones, displaySecond } = this.state;
        return(
            <div className="content-box">
            <form method="POST" id="company-form" noValidate onSubmit={this.handleSubmit}>
                <div className="row">
                        <CSRFToken setToken={this.setToken}/>
                        {
                            fieldConfig.map(({id, name, placeholder, required, type}) => {
                                return(<div className="col-12 col-sm-6">
                                        <label htmlFor={name}>{placeholder}</label><br/>
                                        <input 
                                            id={id}
                                            className="form-control"
                                            name={name}
                                            value={this.state[name]}
                                            required={required}
                                            type={type}
                                            maxLength="254"
                                            title=""
                                            placeholder={placeholder}
                                            onChange={this.handleChange}
                                        /><br/>
                                    </div>)
                                
                                
                            })
                        }
                        <div className="col-12 col-sm-6">
                        <label htmlFor="timezone">TimeZone</label><br/>
                        <select
                            id="timezone" 
                            className="form-control"
                            name="timezone"
                            value={timezone || ""}
                            required
                            onChange={this.handleChange}
                        >
                            <option value="">--Select--</option>
                            {
                                timezones.length > 0 && timezones.map(tz => {
                                    return(
                                        <option key={tz.id} value={tz.id}>{tz.utc}</option>
                                    )
                                })
                            }
                        </select>
                    </div>
                    <div className="col-12 col-sm-6">
                        <label htmlFor="status">Status</label><br/>
                        <select
                            id="status" 
                            className="form-control"
                            name="status"
                            value={status|| "active"}
                            onChange={this.handleChange}
                            required
                        >
                            <option value="active">Active</option>
                            <option value="inactive">Inactive</option>
                        </select>
                    </div>
                </div>
                
                <hr />
                <i class="os-icon os-icon-coins-4 mx-1 text-primary" style={{float: 'right'}} onClick={() => this.setState({ displaySecond: true })} ></i>
                <AddressForm />
                { displaySecond && 
                    <Fragment>
                         <i class="os-icon os-icon-cancel-circle text-danger" style={{float: 'right'}} onClick={() => this.setState({ displaySecond: false })}></i>
                         <AddressForm />
                    </Fragment>        
                    }
                <hr />
                <br />
                <button className="btn btn-primary float-right"><i className="far fa-check-double"></i> Submit Form</button>
            </form>
        </div>
        )
    }
};

export default CompanyForm;