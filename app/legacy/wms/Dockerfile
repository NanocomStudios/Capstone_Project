FROM gcr.io/distroless/java17-debian12

WORKDIR .
COPY . ./wms.jar

EXPOSE 8000

ENTRYPOINT ["java", "-jar", "wms.jar", "8000"]