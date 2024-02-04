FROM centos:7

RUN yum update -y && \
    yum install -y httpd && \
    yum clean all && \
    rm -rf /var/cache/yum


CMD ["httpd", "-D", "FOREGROUND"]
