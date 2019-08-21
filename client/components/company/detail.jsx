import React, { Fragment, useState, useEffect, useCallback } from 'react';

const CompanyDetail = ({ currentCompany, fetchCompanyDetail,  ...routeParams }) => {
    const { match: {params: { companyId }}} = routeParams;
    const [ timezone, setTimezoneState ] = useState('');
    const [ addresses, setAddresses ] = useState([])
    fetchCompanyDetail(companyId);
    let allCompanyAddress = [];

    useEffect(() => {
        currentCompany.timezone &&
        fetch(`/api/core/timezone/${currentCompany.timezone}`)
            .then(result => result.json())
            .then(data => setTimezoneState(data.utc))

    }, []);

    useEffect(() => {
        allCompanyAddress = Object.keys(currentCompany).length > 0 && currentCompany.addresses && currentCompany.addresses.length > 0
        && currentCompany.addresses.map(address => {
            console.log(address)
            return fetch(`/api/core/address/${address}/?company=${currentCompany.id}`)
                        .then(result => result.json())
                        .then(data =>data)
        });

    Promise.all(allCompanyAddress).then(result => {
        setAddresses(result)})
    }, [currentCompany])
    console.log(addresses)

    return(
        <div class="row">
            {
                Object.keys(currentCompany).length > 0?
                (
                <Fragment>
                <div class="element-wrapper">
                <div class="element-box"><h6 class="element-header">{currentCompany.name || 'NA'}</h6>
                    <div class="timed-activities compact">
                        <div class="timed-activity">
                            <div class="ta-date"><span>{currentCompany.phone || 'NA'} / {currentCompany.email || 'NA'}</span></div>
                            <div class="ta-record-w">
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Website</strong></div>
                                    <div class="ta-activity">{currentCompany.website || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Facebook</strong></div>
                                    <div class="ta-activity">{currentCompany.facebook || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Twitter</strong></div>
                                    <div class="ta-activity">{currentCompany.twitter || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Linkedin</strong></div>
                                    <div class="ta-activity">{currentCompany.linkedin || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Instagram</strong></div>
                                    <div class="ta-activity">{currentCompany.instagram || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Youtube</strong></div>
                                    <div class="ta-activity">{currentCompany.youtube || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Timezone</strong></div>
                                    <div class="ta-activity">{timezone || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Status</strong></div>
                                    <div class="ta-activity">{currentCompany.status || ''}</div>
                                </div>
                                <div class="ta-record">
                                    <div class="ta-timestamp"><strong>Website</strong></div>
                                    <div class="ta-activity">{currentCompany.website || ''}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="element-wrapper">
                <div class="element-box"><h6 class="element-header">{currentCompany.name || 'NA'} Addresses</h6>
                    <div class="timed-activities compact">
                        {addresses.length> 0 && addresses.map(add => {
                            return(
                                <div class="timed-activity">
                                    <div class="ta-date"><span class="text-success">{ add.line_1 } ({ add.type })</span></div>
                                    <div class="ta-record-w">
                                        <div class="ta-record">
                                            <div class="ta-timestamp"><strong>{ add.line_1 } { add.line_2||'' } <br/>{ add.city } { add.zip } { add.state }<br/>{ add.country } </strong></div>
                                        </div>
                                    </div>
                                </div>
                            )
                        })}
                </div>
            </div>
        </div>
        </Fragment>
        )
        : 'Loading'
        }
            
    </div>
    )
}

export default CompanyDetail;