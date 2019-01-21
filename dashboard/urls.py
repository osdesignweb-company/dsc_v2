from django.conf.urls import url, include
from dashboard import views

#Importar vistas del app formularios
from formularios.views import formulario_view, export_users_excel

urlpatterns = [
    url(r'^dashboard/$', views.DashboardView, name='dashboard'),
    url(r'^perfil/$', views.CambiarPerfilUsuarioView, name="perfil"),
    url(r'^crear_persona/$', views.CrearPersonaView, name="crear_persona"),
    url(r'^personas/', views.PersonasList.as_view(), name="personas"),
    url(r'^cambiar_password/', views.CambiarPasswordView, name="cambiar_password"),
    url(r'^persona/(?P<id_persona>\w+)/$', views.PersonaUnicaView, name="persona_unica"),
    url(r'^borrar_persona/(?P<id_persona>\w+)/$', views.BorrarUsuarioView, name="borrar_persona"),   
    url(r'^formulario_registro_usuarios/', formulario_view, name="formulario"), 
    url(r'^metricas_registro_usuarios/', views.MetricasRegistroUsuariosView, name="metricas"), 
    url(r'^eliminar_formulario_registro_usuarios/(?P<id_form>\w+)/$', views.BorrarFormlarioView, name="borrar_formulario"), 
    url(r'^test/', views.Test, name="test"), 
    url(r'^export_users_excel/(\d+)/$', export_users_excel, name="export_users_excel")
]
