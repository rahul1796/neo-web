var varTable;
$(document).ready(function () {
    $("#alternative-page-datatable").dataTable().fnDestroy();
	$('.dropdown-search-filter').select2({
                placeholder:''
            });
	LoadRegionddl();
	LoadQPddl();
    LoadTable();      

  /*  $("#alternative-page-datatable").DataTable({
		pagingType: "full_numbers",
		drawCallback: function () {
			$(".dataTables_paginate > .pagination").addClass("pagination-rounded")
		}
    })*/
});
function LoadRegionddl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Region"
        $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
        success: function (data){
            if(data.Region != null)
            {
                $('#ddlRegion').empty();
                var count=data.Region.length;
                if( count> 0)
                {
                    $('#ddlRegion').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlRegion').append(new Option(data.Region[i].Region_Name,data.Region[i].Region_Id));
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


//LoadClusterddl
function LoadClusterddl(){
    var URL=$('#hdn_web_url').val()+ "/Get_all_Cluster_Based_On_Region"
        $.ajax({
        type:"POST",
        url:URL,
        async:false,       
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json", 
        data:{
            "region_id" : $('#ddlRegion').val().toString()//$('#ddlProject option:selected').val()
        },
		success: function (data){
            if(data.ClusterOnRegion != null)
            {
                $('#ddlCluster').empty();
                var count=data.ClusterOnRegion.length;
                if( count> 0)
                {
                    $('#ddlCluster').append(new Option('ALL','-1'));
                    for(var i=0;i<count;i++)
                        $('#ddlCluster').append(new Option(data.ClusterOnRegion[i].Cluster_Name,data.ClusterOnRegion[i].Cluster_Id));
                    //$('#ddlCourse').val('-1');
                }
                else
                {
                    $('#ddlCluster').append(new Option('ALL','-1'));
                }
            }
        },
        error:function(err)
        {
            alert('Error while loading Cluster! Please try again');
            return false;
        }
    });
    return false;
}

	
    function LoadCenter()
    {
        
        var URL=$('#hdn_web_url').val()+ "/AllCenterList";
        $.ajax({
            type:"GET",
            url:URL,
            async:false,        
            beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
            datatype:"json",
			"data": {cluster_id : $('#ddlCluster').val().toString()},
            success: function (data){
                if(data.Centers != null)
                {
                    $('#ddlCenter').empty();
                    var count=data.Centers.length;
                    if( count> 0)
                    {
                        $('#ddlCenter').append(new Option('ALL','0'));
                        for(var i=0;i<count;i++)
                            $('#ddlCenter').append(new Option(data.Centers[i].Center_Name,data.Centers[i].Center_Id));
                        //$('#ddlCenterType').val('');
                    }
                    else
                    {
                        $('#ddlCenter').append(new Option('ALL','0'));
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
function LoadQPddl()
{
    var URL=$('#hdn_web_url').val()+ "/AllQPBasedOnSector"
	//alert($('#ddlSector').val().toString())
    $.ajax({
        type:"GET",
        url:URL,
        async:false,        
        beforeSend:function(x){ if(x && x.overrideMimeType) { x.overrideMimeType("application/json;charset=UTF-8"); } },
        datatype:"json",
		"data": {sector_id : ''},
		success: function (data){
            if(data.QP != null)
                {	
                    $('#ddlQP').empty();
                    var count=data.QP.length;
					//alert(count)
                    if( count> 0)
                    {
                        $('#ddlQP').append(new Option('ALL',''));
                        for(var i=0;i<count;i++)
                            $('#ddlQP').append(new Option(data.QP[i].Qp_Name,data.QP[i].Qp_Id));
                    }
                    else
                    {
                        $('#ddlQP').append(new Option('ALL',''));
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
    vartable1 = $("#alternative-page-datatable").DataTable({
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
            "url": $('#hdn_web_url').val()+ "/project_list",
            "type": "POST",
            "dataType": "json",
            "data": function (d) {
                d.project_id = 0;
				d.region_ids = $('#ddlRegion').val().toString();
				d.cluster_id = $('#ddlCluster').val().toString();
				d.center_id = $('#ddlCenter').val().toString();
				d.qp = $('#ddlQP').val().toString();
            },
            error: function (e) {
                $("#alternative-page-datatable tbody").empty().append('<tr class="odd"><td valign="top" colspan="16" class="dataTables_empty">ERROR</td></tr>');
            }

        },

        "columns": [
            { "data": "S_No"},
            { "data": "Project_Name" },
            { "data": "Contract_Name" },
            { "data": "Client_Name" },            
            { "data": "Practice_Name"},
            {"visible": false,
            "data": function (row, type, val, meta) {
            var varButtons = ""; 
            varButtons += '<a onclick="EditProjectDetail(\'' + row.Project_Id + '\')" class="btn" style="cursor:pointer" ><i title="Edit Project" class="fas fa-edit" ></i></a>';
            return varButtons;
            }
            }
        ],
        drawCallback: function(){
            $('#alternative-page-datatable_paginate ul.pagination').addClass("pagination-rounded");
        }

    });
}
function EditProjectDetail(ProjectId)
{
    $('#hdn_project_id').val(ProjectId);
    $('#form1').submit();
    
}