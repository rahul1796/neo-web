var varTable;
$(document).ready(function () {
    $("#imgSpinner").hide();
    $('.dropdown-search-filter').select2();
    $(".date-picker").flatpickr({
        dateFormat:'d-M-Y',
        minDate: '01.Apr.2019'
    });
    $("#tbl_candidate").dataTable().fnDestroy();
    Loadcandidatestatusddl();
    LoadCenterType();
    LoadRegionddl();
    loadClient();
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 5)
        $('#btn_create').hide();
    //LoadTable();
});

function Loadcandidatestatusddl(){
    if (($('#FromDate').val()=='')|($('#ToDate').val()==''))
    {   
        $("#ddlstatus_div").hide();
        $('#ddlcandidateStage').val("");
    }
    else
    {
        $("#ddlstatus_div").show();
        $('#ddlcandidateStage').empty();
        $('#ddlcandidateStage').append(new Option('Enrolled','1'));
        $('#ddlcandidateStage').append(new Option('Certified','2'));
        $('#ddlcandidateStage').append(new Option('Placed','3'));
    }    
}
function LoadRegionddl(){
    var URL=$('#hdn_web_url').val()+ "/AllRegionsBasedOnUser"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id" : $('#hdn_home_user_role_id').val(),
            "user_region_id" : $('#hdn_user_region_id').val()
        },

        success: function (data){
            if(data.Regions != null)
            {
                $('#ddlRegion').empty();
                var count=data.Regions.length;
                if( count> 0)
                {
                    //$('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlRegion').append(new Option(data.Regions[i].Region_Name,data.Regions[i].Region_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlRegion').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading BU! Please try again');
            return false;
        }
    });
    return false;
}

function loadClient(){
    var URL=$('#hdn_web_url').val()+ "/GetALLClient"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
        },
        success: function (data){
            if(data.Clients != null)
            {
                $('#ddlClient').empty();
                var count=data.Clients.length;
                if( count> 0)
                {
                    //$('#ddlClient').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlClient').append(new Option(data.Clients[i].Customer_Name,data.Clients[i].Customer_Id));
                }
                else
                {
                    $('#ddlClient').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            //alert($('#ddlClient').val().toString())
            alert('Error! Please try again');
            return false;
        }
    });
}
function loadbasedonclient()
{
    //alert($('#ddlClient').val().toString());
    LoadContract();
    LoadProject();
}
function LoadContract(){

    var URL=$('#hdn_web_url').val()+ "/GetContractsBasedOnCustomer"  //"/GetALLProject_multiple"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "customer_id":$('#ddlClient').val().toString(),
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
        },
        success: function (data){
            if(data.Contracts != null)
            {
                $('#ddlContract').empty();
                var count=data.Contracts.length;
                if( count> 0)
                {
                    //$('#ddlProject').append(new Option('ALL','-1'));  , 
                    for(var i=0;i<count;i++)
                        $('#ddlContract').append(new Option(data.Contracts[i].Contract_Name,data.Contracts[i].Contract_Id));
                }
                else
                {
                // $('#ddlContract').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(request, err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadCenterType()
{       
    var URL=$('#hdn_web_url').val()+ "/AllCenterTypes"
    $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
                "user_id": $('#hdn_home_user_id').val(),
                "user_role_id" : $('#hdn_home_user_role_id').val()
        },
        success: function (data){
            if(data.Center_Types != null)
            {
                $('#ddlCenterType').empty();
                var count=data.Center_Types.length;
                if( count> 0)
                {
                    for(var i=0;i<count;i++)
                        $('#ddlCenterType').append(new Option(data.Center_Types[i].Center_Type_Name,data.Center_Types[i].Center_Type_Id));                    
                }
                else
                {
                    $('#ddlCenterType').append(new Option('ALL',''));
                }
                $("#ddlCenterType option[value='']").attr('disabled','disabled');
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadProject(){
    var URL=$('#hdn_web_url').val()+ "/GetALLProject_multiple"  //"/GetALLProject_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ClientId":$('#ddlClient').val().toString(),
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
        },
        success: function (data){
            if(data.Projects != null)
            {
                $('#ddlProject').empty();
                var count=data.Projects.length;
                if( count> 0)
                {
                    //$('#ddlProject').append(new Option('ALL','-1'));  , 
                    for(var i=0;i<count;i++)
                        $('#ddlProject').append(new Option(data.Projects[i].Project_Name,data.Projects[i].Project_Id));
                }
                else
                {
                    $('#ddlProject').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(request, err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}
function LoadSubProject(){
    //alert($('#ddlProject').val().toString())
    var URL=$('#hdn_web_url').val()+ "/get_subproject_basedon_proj_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "ProjectId":$('#ddlProject').val().toString(),
            "user_id": $('#hdn_home_user_id').val(),
            "user_role_id": $('#hdn_home_user_role_id').val()
        },
        success: function (data){
            if(data.Sub_Project != null)
            {
                $('#ddlSubProject').empty();
                var count=data.Sub_Project.length;
                if( count> 0)
                {
                    //$('#ddlCourse').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlSubProject').append(new Option(data.Sub_Project[i].Sub_Project_Name,data.Sub_Project[i].Sub_Project_Id));
                }
                else
                {
                    $('#ddlSubProject').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}

function LoadCenter(){
    var URL=$('#hdn_web_url').val()+ "/get_cand_center_basedon_course_multiple"
    $.ajax({
        type:"POST",
        url:URL,
        async:false,
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "CourseId":"",
            "RegionId":$('#ddlRegion').val().toString()
        },
        success: function (data){
            if(data.Centers != null)
            {
                $('#ddlCenter').empty();
                var count=data.Centers.length;
                if( count> 0)
                {
                    //$('#ddlCenter').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCenter').append(new Option(data.Centers[i].Center_Name,data.Centers[i].Center_Id));
                }
                else
                {
                    $('#ddlCenter').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {   
            
            alert('Error! Please try again');
            return false;
        }
    });
    return false;
}

function LoadTable()
{
    var course_selected="",data='';
    var count;
    
    vartable1 = $("#tbl_candidate").DataTable({
        "serverSide": true,
        "aLengthMenu": [[10, 25, 50], [10, 25, 50]],
        "paging": true,
        "pageLength": 10,
        "sPaginationType": "full_numbers",
        "scrollX": false,
        "destroy": true,
        "processing": true,
        "language": { "processing": 'Loading..!' },
        "ajax": {
            "url": $('#hdn_web_url').val()+ "/candidate_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.candidate_id = 0;
		        d.user_id = $('#hdn_home_user_id').val();
                d.user_role_id  = $('#hdn_home_user_role_id').val();
                d.status = $('#ddlStatus').val().toString();
                d.customer = $('#ddlClient').val().toString();
                d.project = $('#ddlProject').val().toString();
                d.sub_project = $('#ddlSubProject').val().toString();
                d.region = $('#ddlRegion').val().toString();
                d.center = $('#ddlCenter').val().toString();
                d.center_type = $('#ddlCenterType').val().toString();
                d.Contracts = $('#ddlContract').val().toString();
                d.candidate_stage = $('#ddlcandidateStage').val().toString();
                d.from_date = $('#FromDate').val();
                d.to_date = $('#ToDate').val();  
            },
            error: function (e) {
                $("#tbl_candidate tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": function (row, type, val, meta) {
                varHtml=row.First_Name+" "+row.Middle_Name+" "+row.Last_Name;
                varButtons = '<a onclick="CandidateBasicDetails(\'' + row.First_Name + '\',\'' + row.Middle_Name + '\',\'' + row.Last_Name + '\',\'' + row.Salutation + '\',\'' + row.Date_Of_Birth+ '\',\'' + row.Age+ '\',\'' + row.Gender+ '\',\'' + row.Marital_Status+ '\',\'' + row.Caste+ '\',\'' + row.Disability_Status+ '\',\'' + row.Religion+ '\',\'' + row.Interested_Course+ '\')"  style="color:blue;cursor:pointer" >'+row.First_Name+'</a>';
                return varButtons;
                }
            },
            { "data": "Source_Of_Information"},
            {       
                "data": function (row, type, val, meta) {
                    
                    var varButtons='<a onclick="CandidateContactDetails(\'' + row.Primary_Contact_No+ '\',\'' + row.Secondary_Contact_No+ '\',\'' + row.Email_Id+ '\',\'' + row.Present_Address_Line1+ '\',\'' + row.Present_Address_Line2+ '\',\'' + row.Present_Village+ '\',\'' + row.Present_Panchayat+ '\',\'' + row.Present_Taluk_Block+ '\',\'' + row.Present_District+ '\',\'' + row.Present_State_Name+ '\',\'' + row.Present_Pincode+ '\',\'' + row.Present_Country_Name+ '\',\'' + row.Permanaet_Address_Line1+ '\',\'' + row.Permanent_Address_Line2+ '\',\'' + row.Permanent_Village+ '\',\'' + row.Permanent_Panchayat+ '\',\'' + row.Permanent_Taluk_Block+ '\',\'' + row.Permanent_District+ '\',\'' + row.Permanent_State_Name+ '\',\'' + row.Permanent_Pincode+ '\',\'' + row.Permanent_Country_Name+ '\')"  style="color:blue;cursor:pointer" >Click Here</a>';
                    return varButtons;
                }
            },
            {       
                "data": function (row, type, val, meta) {
                    var varButtons='<a onclick="CandidateExperienceDetails(\'' + row.Highest_Qualification+ '\',\'' + row.Stream_Specialization+ '\',\'' + row.Technical_Knowledge+ '\',\'' + row.Computer_Knowledge+ '\',\'' + row.Name_Of_Institute+ '\',\'' + row.University+ '\',\'' + row.Year_Of_Pass+ '\',\'' + row.Percentage+ '\',\'' + row.Employment_Type+ '\',\'' + row.Preferred_Job_Role+ '\',\'' + row.Relevant_Years_Of_Experience+ '\',\'' + row.Current_Last_Ctc+ '\',\'' + row.Preferred_Location+ '\',\'' + row.Willing_To_Travel+ '\',\'' + row.Willing_To_Work_In_Shifts+ '\',\'' + row.Expected_Ctc+ '\')"  style="color:blue;cursor:pointer" >Click Here</a>';
                    return varButtons;
                }
            },
            
            {      
                "data": function (row, type, val, meta) {
                    var varButtons='<a onclick="CandidateIDDetails(\'' + row.Aadhar_No+ '\',\'' + row.Identifier_Type+ '\',\'' + row.Identity_Numbe+ '\')"  style="color:blue;cursor:pointer" >Click Here</a>';
                    return varButtons;
                }
            }
            
        ],
        drawCallback: function(){
            $('#tbl_candidate_paginate ul.pagination').addClass("pagination-rounded");
        }


    });
}


function LoadTableBasedOnSearch(){
    
    $("#tbl_candidate").dataTable().fnDestroy();
    LoadTable(); 
}

function CandidateBasicDetails(FirstName,MiddleName,LastName,Salutation,Dob,Age,gender,MaritalStatus,Caste,Disability,religion,InterestedCourse)
{
    $('#txtSalutation').val(Salutation);
    $('#txtFirstName').val(FirstName);
    $('#txtMiddleName').val(MiddleName);
    $('#txtLastName').val(LastName);
    $('#txtDob').val(Dob);
    $('#txtAge').val(Age);
    $('#txtgender').val(gender);
    $('#txtMaritalStatus').val(MaritalStatus);
    $('#txtCaste').val(Caste);
    $('#txtDisability').val(Disability);
    $('#txtReligion').val(religion);    
    $('#txtCourse').val(InterestedCourse);
    $('#mdl_cand_basic').modal('show');
}
function CandidateContactDetails(primary_contact,SecondaryContact,Email,PresnetAdd1,PresentAdd2,PresentVillage,PresentPanchayat,presentTalukBlock,PresentDist,PresentState,PresentPin,PresentCon,PermanentAdd1,PermanentAdd2,PermanentVillage,PermanentPanchayat,PermanentTalukBlock,PermanentDist,PermanentState,PermanentPin,PermanentCon)
{    
    $('#txtPrCont').val(primary_contact);    
    $('#txtSecondary').val(SecondaryContact); 
    $('#txtEmail').val(Email); 
    $('#txtPrAdd1').val(PresnetAdd1); 
    $('#txtPrAdd2').val(PresentAdd2); 
    $('#txtPrVillage').val(PresentVillage);
    $('#txtPrPanchayat').val(PresentPanchayat);
    $('#txtPrBloack').val(presentTalukBlock);
    $('#txtPrDistrict').val(PresentDist);
    $('#txtPrState').val(PresentState);
    $('#txtPrPin').val(PresentPin);
    $('#txtPrCon').val(PresentCon);
   
    $('#txtPerAdd1').val(PermanentAdd1); 
    $('#txtPerAdd2').val(PermanentAdd2); 
    $('#txtPerVillage').val(PermanentVillage);
    $('#txtPerPanchayat').val(PermanentPanchayat);
    $('#txtPerBloack').val(PermanentTalukBlock);
    $('#txtPerDistrict').val(PermanentDist);
    $('#txtPerState').val(PermanentState);
    $('#txtPerPin').val(PermanentPin);
    $('#txtPerCon').val(PermanentCon);
    $('#mdl_cand_contact').modal('show');
}
function CandidateExperienceDetails(Highest_Qualification,Stream_Specialization,Technical_Knowledge,Computer_Knowledge,Name_Of_Institute,University,Year_Of_Pass,Percentage,Employment_Type,Preferred_Job_Role,Relevant_Years_Of_Experience,Current_Last_Ctc,Preferred_Location,Willing_To_Travel,Willing_To_Work_In_Shifts,Expected_Ctc)
{
    
    $('#txtHighestQua').val(Highest_Qualification);
    $('#txtStream').val(Stream_Specialization);
    $('#txttechKnow').val(Technical_Knowledge);
    $('#txtComKnow').val(Computer_Knowledge);
    $('#txtInstitute').val(Name_Of_Institute);
    $('#txtUniversiry').val(University);
    $('#txtPassYr').val(Year_Of_Pass);
    $('#txtPer').val(Percentage);
    
    $('#txtEmpType').val(Employment_Type);
    $('#txtPreferred').val(Preferred_Job_Role);
    $('#txtRel').val(Relevant_Years_Of_Experience);
    $('#txtCurCTC').val(Current_Last_Ctc);
    $('#txtPreLoc').val(Preferred_Location);
    $('#txtWillingTravel').val(Willing_To_Travel);
    $('#txtshifts').val(Willing_To_Work_In_Shifts);
    $('#txtExpCTC').val(Expected_Ctc);
    $('#mdl_cand_experience').modal('show');
}

function CandidateIDDetails(Aadhar_No,    Identifier_Type,    Identity_Numbe)
{    
    $('#txtAadhar').val(Aadhar_No);
    $('#txtIdentificationType').val(Identifier_Type);
    $('#txtIdenNumber').val(Identity_Numbe);
    $('#mdl_cand_identity').modal('show');
}


function DownloadTableBasedOnSearch(){
    $("#imgSpinner").show();
    /*if($('#ddlCustomer').val()==''|| $('#ddlCustomer').val()==null){
        alert("Please select a Customer.");
    
    }
    else if($('#ddlCenter').val()==''|| $('#ddlCenter').val()==null){
        alert("Please select a Center.");
    
    }
    else if($('#ddlCourse').val()==''|| $('#ddlCourse').val()==null){
        alert("Please select a Center.");
    
    }
    */
    if (0==9){
    console.log(false)
    }
    else{
        var URL=$('#hdn_web_url').val()+ "/candidate_download_report"
        //window.location = URL + "?ActivityDate=2019-09-09"
        $.ajax({
                    type: "POST",
                    dataType: "json",
                    url: URL, 
                    data: {
                            //candidate_id, user_id, user_role_id, status, customer, project, sub_project, region, center, center_type
                            'candidate_id':0,
                            'user_id':$('#hdn_home_user_id').val(),
                            'user_role_id':$('#hdn_home_user_role_id').val(),
                            'status':$('#ddlStatus').val().toString(),
                            'customer':$('#ddlClient').val().toString(),
                            'project': $('#ddlProject').val().toString(),
                            'sub_project':$('#ddlSubProject').val().toString(),
                            'region':$('#ddlRegion').val().toString(),
                            'center':$('#ddlCenter').val().toString(),
                            'center_type':$('#ddlCenterType').val().toString(),
                            'Contracts' :$('#ddlContract').val().toString(),
                            'candidate_stage':$('#ddlcandidateStage').val().toString(),
                            'from_date' : $('#FromDate').val(),
                            'to_date' : $('#ToDate').val()

                    },
                    success: function(resp) 
                    {

                        if (resp.Status){
                            var varAnchor = document.getElementById('lnkDownload');
                            varAnchor.href = $('#hdn_web_url').val() + '/report file/' + resp.filename;
                            $("#imgSpinner").hide();
                            try 
                                { 
                                    //in firefox
                                    varAnchor.click();
                                    return;
                                } catch(ex) {}
                                
                                try 
                                { 
                                    // in chrome
                                    if(document.createEvent) 
                                    {
                                        var e = document.createEvent('MouseEvents');
                                        e.initEvent( 'click', true, true );
                                        varAnchor.dispatchEvent(e);
                                        return;
                                    }
                                } catch(ex) {}
                                
                                try 
                                { 
                                    // in IE
                                    if(document.createEventObject) 
                                    {
                                         var evObj = document.createEventObject();
                                         varAnchor.fireEvent("onclick", evObj);
                                         return;
                                    }
                                } catch(ex) {}
                            
                        }
                        else{
                            //alert(resp.Description)
                            //alert('Not success')
                            $("#imgSpinner").hide();
                            
                        }
                    },
                    error:function()
                    {
                        //$("#imgSpinner").hide();
                    }
                });
        
    }
    //$("#imgSpinner").hide();
}

function ForceDownload(varUrl, varFileName)
        {
            var link = document.createElement('a');
            link.setAttribute('href', varUrl);
            link.setAttribute('download', varFileName);
            link.setAttribute('target', '_blank');
            link.style.display = 'none';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }