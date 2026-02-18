FROM gcr.io/distroless/java17-debian12

WORKDIR /app
COPY wms.jar /app/

EXPOSE 8000

ENTRYPOINT ["java", "-jar", "wms.jar", "8000"]