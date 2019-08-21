import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route } from 'react-router-dom'; 


// components
import CompanySectionHeader from '../components/company/header';
import CompanyAdd from '../components/company/add';
import CompanyDelete from '../components/company/delete';
import CompanyEdit from '../components/company/edit';
import CompanyDetail from '../components/company/detail';
import CompanyList from '../components/company/list';
import Page404 from '../components/page404';

const App = () => {
    const [ companies, setCompanies ] = useState([]);
    const [ currentCompany, setCurrentCompany ] = useState({});
    useEffect(() => {
        fetch('/api/core/company')
            .then((result)=> result.json())
            .then((data) => setCompanies(data.results))
    }, [])

    let fetchCompanyDetail = (companyId) => {
        useEffect(() => {
            fetch(`/api/core/company/${companyId}`)
            .then(result => result.json())
            .then(data => {
                // console.log(data)
                setCurrentCompany(data)})
        }, [])
    }
    return(
        <div className="content-box">
            <div className="element-wrapper">
                <div className="element-box">
                    <BrowserRouter basename="/company">
                            <div>
                                <CompanySectionHeader />
                                <Route path="/add" exact render={props => <CompanyAdd {...props} />}></Route>
                                <Route path="/delete/:companyId" exact render={props => <CompanyDelete {...props} />}></Route>
                                <Route path="/edit/:companyId" exact render={props => <CompanyEdit {...props} />}></Route>
                                <Route path="/detail/:companyId" exact render={props => 
                                <CompanyDetail {...props} 
                                    fetchCompanyDetail={fetchCompanyDetail}
                                    currentCompany={currentCompany}
                                    />}>
                                </Route>
                                <Route path="/list" exact render={props => <CompanyList {...props} companies={companies}/>}></Route>
                            </div>
                    </BrowserRouter>
                </div>
            </div>
        </div>
    
    )
}

export default App;