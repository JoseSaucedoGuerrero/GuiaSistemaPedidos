from django.db import models
from pos_project.choices import EstadoEntidades
import uuid

# Create your models here.

class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_grupo = models.CharField(max_length=5, null=False)
    nombre_grupo = models.CharField(max_length=50, null=False)
    estado = models.IntegerField(choices=EstadoEntidades.choices, default=EstadoEntidades.ACTIVO)
    
    def __str__(self):
        return self.nombre_grupo
    
    class Meta:
        db_table = "grupos_articulos"
        ordering = ["codigo_grupo"]


class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo_linea = models.CharField(max_length=10, null=False)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_linea')
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades.choices, default=EstadoEntidades.ACTIVO)
    
    def __str__(self):
        return self.nombre_linea
    
    class Meta:
        db_table = "lineas_articulos"
        ordering = ["codigo_linea"]
        