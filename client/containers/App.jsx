import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom'; 


// components
import Dashboard from '../components/dashboard';
import Company from './Company';
import CompanySectionHeader from '../components/company/header';
import CompanyAdd from '../components/company/add';
import CompanyDelete from '../components/company/delete';
import CompanyEdit from '../components/company/edit';
import CompanyDetail from '../components/company/detail';
import CompanyList from '../components/company/list';
import Page404 from '../components/page404';

const App = () => {
    const [ companies, setCompanies ] = useState([]);
    useEffect(() => {
        fetch('/api/core/company')
            .then((result)=> result.json())
            .then((data) => setCompanies(data.results))
    }, [])
    return(
      
       <BrowserRouter>
            <Switch>
                <Route path="/dashboard" exact render={props => <Dashboard  {...props}/>}></Route>
                <Route path="/company"  render={props => <Company {...props}/>}></Route>
                <Page404 />
            </Switch>
       </BrowserRouter>
    
    )
}

export default App;