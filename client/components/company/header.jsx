import React from 'react';
import { Link, withRouter } from 'react-router-dom';

const CompanySectionHeader = (props) => {
    const { location: { pathname } } = props;
    const pathTest = pathname.split('/')[1];
    let title, linkPath, linkName, id = '';

    switch(pathTest) {
        case "add":
            title = "New Company";
            linkPath = "/list";
            linkName = "Companies";
            break;

        case "list":
            title = "Manage Companies";
            linkPath = "/add";
            linkName = "Add Company";
            break;
        
        case "edit":
            title = "Edit Company";
            linkPath = "/list";
            linkName = "Companies";
            break;
        
        
        case "detail":
            title = "View Company";
            linkPath = "/list";
            linkName = "Companies";
            break;

        case "delete":
            break;

    }
    
    return(
        <h5 class="form-header">
        <i class="fa fa-id-card-o"></i> { title }

    <small>
        <Link to={`${linkPath}/${id}`} title="View Companies" data-toggle='tooltip' class="float-right"><i class="fal fa-list"></i> {linkName}</Link>
    </small>
    </h5>
    )
}

export default withRouter(CompanySectionHeader);