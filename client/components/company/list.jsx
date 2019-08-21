import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';

const CompanyList = ({ companies }) => {
    return(
        
            <div className="table-responsive">
                    <table id="company-table" width="100%" className="table table-striped table-sm table-lightfont">
                        <thead>
                            <tr>
                                <th className="text-center">Edit</th>
                                <th className="text-center">View</th>
                                <th>Status</th>
                                <th>Name</th>
                                <th>City</th>
                                <th>State</th>
                                <th>Phone</th>
                            </tr>
                        </thead>
                        <tbody>
                                {
                                    companies.length>0 && 
                                    companies.map(({id, status, name, phone, }) => {
                                        return(
                                            <tr key={id}>
                                            <td data-type="Status"><Link to={`/edit/${id}`} title="Edit" data-toggle="tooltip"><i className="os-icon os-icon-pencil-1"></i> </Link></td>
                                            <td className="px-0 text-center"><Link to={`/detail/${id}`} title="View" data-toggle="tooltip">{name}</Link></td>
                                            <td data-type="Status">{status}</td>
                                            <td data-type="Name">
                                                    {
                                                        name === 'Savy Bizz'?
                                                        <Fragment>
                                                            <Link
                                                            to="" title='Stop impersonating '
                                                            data-toggle='tooltip'
                                                            className="impersonate text-danger"
                                                            data-company="Savvy Biz">
                                                            <i className="far fa-person-carry mr-2"></i>
                                                            </Link>
                                                            <b>{name}</b>
                                                        </Fragment>
                                                        
                                                    :
                                                        <Fragment>
                                                             <Link
                                                                to=""
                                                                title='Start impersonating '
                                                                data-toggle='tooltip'
                                                                className="impersonate text-primary"
                                                                data-company="">
                                                                <i className="fas fa-person-carry mr-2">
                                                                </i>
                                                            </Link>
                                                            {name}
                                                        </Fragment>
                                                    }
                                            </td>
                                            <td data-type="City">Placeholder City</td>
                                            <td data-type="State">Placeholder State</td>
                                            <td data-type="Phone">{phone}</td>
                                        </tr>
                                        )
                                    })
                                }
                        </tbody>
                    </table>
                </div>
    )
}

export default CompanyList;