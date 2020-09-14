var varTable;
$(document).ready(function () {
    $("#tbl_qp").dataTable().fnDestroy();
	$('.dropdown-search-filter').select2({
                placeholder:''
            });
	
	
	LoadSector()		
    LoadTable(""); 
    role_id=parseInt($('#hdn_home_user_role_id').val());
    if(role_id == 1 || role_id == 16 )
        $('#btn_create').show();
});

function LoadSector()
{
	var URL=$('#hdn_web_url').val()+ "/All_Sector";
        $.ajax({
            type:"GET",
            url:URL,
            async:false,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
            success: function (data){
                if(data.Sectors != null)
                {
                    $('#ddlsector').empty();
                    var count=data.Sectors.length;
                    if( count> 0)
                    {
                        //$('#ddlsector').append(new Option('ALL',''));
                        for(var i=0;i<count;i++)
                            $('#ddlsector').append(new Option(data.Sectors[i].Sector_Name,data.Sectors[i].Sector_Id));
                        //$('#ddlCenterType').val('');
                    }
                    else
                    {
                        $('#ddlsector').append(new Option('ALL',''));
                    }
                    //$("#ddlCenter option[value='0']").attr('disabled','disabled');
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

function LoadTableBasedOnSearch(){      
            LoadTable($('#ddlsector').val().toString());
    }
	
	
function LoadTable(sectors)
{
    vartable1 = $("#tbl_qp").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/qp_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.user_id =$('#hdn_home_user_id').val();
                d.user_role_id = $('#hdn_home_user_role_id').val();
                d.qp_id = 0;
				d.sectors = sectors;
            },
            error: function (e) {
                $("#tbl_qp tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            {"visible": true,
                "data": function (row, type, val, meta) {
                    var varButtons = ""; 
                    if(role_id == 1 || role_id==16)
                        varButtons += '<a onclick="EditQPDetail(\'' + row.Qp_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Client" class="fas fa-edit" ></i></a>';
                    return varButtons;
                }
            },
            { "data": "Qp_Name" },
            { "data": "Qp_Code"},
            { "data": "Sector_Name"},
            { "visible":false,"data": function (row, type, val, meta) {
                var varStatus = ""; 
                if(row.Is_Active)
                    varStatus="Active";
                else
                    varStatus="In Active";
                return varStatus;
                }
            }
        ],
        drawCallback: function(){
            $('#tbl_qp_paginate ul.pagination').addClass("pagination-rounded");
        }


    });
}
function EditQPDetail(QpId)
{
    $('#hdn_qp_id').val(QpId);
    $('#qp_form').submit();
    
}