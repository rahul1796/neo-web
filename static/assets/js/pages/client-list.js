var varTable;
var IsActive;
$(document).ready(function () {
    //IsActive='{{active}}';
    // if ('{{active}}'!="")
    //     IsActive=0;
    console.log(IsActive);
    $("#tbl_clients").dataTable().fnDestroy();
    $('.dropdown-search-filter').select2({
        placeholder:''
    });
    LoadFunding_Resourcesdl();
    LoadCustomer_Groupdl();
    LoadSalesCategoryddl();
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 1)
        $('#btn_create').show();
    else 
        $('#btn_create').hide();

    LoadTable(); 


});


function LoadFunding_Resourcesdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Funding_resources"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Funding_Resources != null)
            {
                $('#ddlFundingSource').empty();
                var count=data.Funding_Resources.length;
                if( count> 0)
                {
                    //$('#ddlFundingSource').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlFundingSource').append(new Option(data.Funding_Resources[i].Funding_Source_Name,data.Funding_Resources[i].Funding_Source_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlFundingSource').append(new Option('ALL','-1'));
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

function LoadCustomer_Groupdl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Customer_Group"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        data:{
            "customer_group_id" : 0 //$('#ddlRM_role').val().toString()//$('#ddlProject option:selected').val()
        },
        success: function (data){
            if(data.Customer_Group != null)
            {
                $('#ddlcustomergroup').empty();
                var count=data.Customer_Group.length;
                if( count> 0)
                {
                    //$('#ddlcustomergroup').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlcustomergroup').append(new Option(data.Customer_Group[i].Customer_Group_Name,data.Customer_Group[i].Customer_Group_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlcustomergroup').append(new Option('ALL','-1'));
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

function LoadSalesCategoryddl(){
    var URL=$('#hdn_web_url').val()+ "/GetAllCategoryTypes"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.CategoryType != null)
            {
                $('#ddlCategoryType').empty();
                var count=data.CategoryType.length;
                if( count> 0)
                {
                    for(var i=0;i<count;i++)
                        $('#ddlCategoryType').append(new Option(data.CategoryType[i].Category_Type_Name,data.CategoryType[i].Category_Type_Id));
                    
                }
                else
                {
                    $('#ddlCategoryType').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading Category Type! Please try again');
            return false;
        }
    });
    return false;
}

function LoadTable()
{
    vartable1 = $("#tbl_clients").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/client_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_id=$('#hdn_home_user_id').val();
                d.user_role_id=$('#hdn_home_user_role_id').val();
                d.client_id = 0;
                d.funding_sources=$('#ddlFundingSource').val().toString();
                d.is_active=-1;
                d.customer_groups = $('#ddlcustomergroup').val().toString();
                d.category_type_ids = $('#ddlCategoryType').val().toString();
            },
            error: function (e) {
                $("#tbl_clients tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }
        },

        "columns": [
            { "data": "S_No"},  
            {"visible": $('#hdn_home_user_role_id').val()=='1'?true:false,
            // function (){
            //     if($('#hdn_home_user_role_id').val()=='1')
            //         return true;
            //     else return false;
            // },
             "data": function (row, type, val, meta) {
                var varButtons = ""; 
                varButtons += '<a onclick="EditClientDetail(\'' + row.Client_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                return varButtons;
                }
            },
            { "data": "Client_Name" },
            { "data": "Client_Code" },
            { "visible":true,
            "data": function (row, type, val, meta) {
                var varButtons = ""; 
                if(row.Poc_Count=="" || row.Poc_Count==0)
                    varButtons=row.Poc_Count;
                else
                {
                    varButtons += '<a onclick="GetPOC(\'' + row.Client_Id + '\',\''+row.Client_Name+ '\')"  style="color:blue;cursor:pointer" >' + row.Poc_Count + '</a>';
                }
                return varButtons;
                }
            },
            { "data": "Funding_Source_Name" },
            { "data": "Customer_Group_Name" },
            { "data": "Category_Type_Name" },
            { "data": "Industry_Type_Name" }
          
        ],
        // "ColumnDefs"  :[
        //     {
        //         "visible": false,
        //         "targets": [ 1 ],                
        //         "searchable": false,
        //         "ordering":false
        //     }
        // ],
        drawCallback: function(){
            $('#tbl_clients_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}
function EditClientDetail(ClientId)
{
    $('#hdn_client_id').val(ClientId);
    $('#form1').submit();
    
}

function GetPOC(customer_id, client_name)
{
    console.log(customer_id)
    $('#HdCustomer').text(client_name);
    var URL=$('#hdn_web_url').val()+ "/GetPOCForCustomer?customer_id="+customer_id;
    $.ajax({
        type:"GET",
        url:URL,
        async:false,
        overflow:true,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            varHtml='';
            $("#tbl_POC_Cusgtomer").dataTable().fnDestroy();
            $("#tbl_POC_Cusgtomer tbody").empty();
            if(!jQuery.isEmptyObject(data))
            {   if (data.POC != null){
                    count=data.POC.length;
                    if (count>0)
                    {   varHtml='';
                        console.log(count);
                        for(var i=0;i<count;i++)
                        {
                            td_open= '  <td style="text-align:center;">' ;
                            td_close=   '</td>';       
                            varHtml+='<tr>';
                            varHtml+='  <td style="text-align:center;">'+ data.POC[i].S_No +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.POC[i].Contact_Person_Name +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.POC[i].Email_Id +'</td>';                    
                            varHtml+='  <td style="text-align:center;">'+ data.POC[i].Number +'</td>';
                            varHtml+='  <td style="text-align:center;">'+ data.POC[i].Designation +'</td>';     
                            varHtml+='</tr>';                            
                        }
                        $("#tbl_POC_Cusgtomer tbody").append(varHtml);
                            $("#tbl_POC_Cusgtomer").DataTable();
                            $('#divPOCList').modal('show');
                            varHtml='';
                    }
                    else
                    {
                        varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                        $("#tbl_POC_Cusgtomer tbody").append(varHtml);
                        $('#divPOCList').modal('show');
                    } 
                    
                }
            }
            else
            {
                varHtml='<tr><td colspan="5" style="text-align:center;">No records found</td></tr>'
                $("#tbl_POC_Cusgtomer tbody").append(varHtml);
                $('#divPOCList').modal('show');
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
