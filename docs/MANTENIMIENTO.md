# Actualización, copias y recuperación

Adapta este procedimiento al proyecto antes de distribuirlo.

## Qué guardar

Documenta rutas reales de datos, base de datos, configuración y archivos del usuario. Distingue código reinstalable de información que no se puede recuperar. Las credenciales requieren almacenamiento privado y cifrado; nunca van al repositorio.

## Antes de actualizar

1. Lee los cambios, requisitos y posibles migraciones.
2. Registra la versión instalada.
3. Crea una copia de datos y configuración en un destino independiente.
4. Si hay bases de datos, utiliza su método de copia coherente; copiar archivos mientras se escriben puede generar una copia inválida.
5. Comprueba que puedes restaurar la copia en un entorno separado.

## Actualizar

Añade aquí los comandos exactos probados para la tecnología del proyecto. Documenta si hay que detener servicios y ejecutar migraciones. No sobrescribas la configuración privada del usuario.

## Verificar

Comprueba arranque, acceso a datos y flujo principal. Registra versión, fecha y resultado.

## Recuperar

Documenta cómo detener la aplicación, restaurar datos/configuración y usar la versión compatible. Una migración puede impedir volver a una versión anterior: define la recuperación antes de actualizar.

## Política de copias

Completa frecuencia, retención, destino, responsable y fecha de la última prueba de restauración. Protege los datos sensibles y mantén al menos una copia independiente del dispositivo.
