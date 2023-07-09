# Set Image
FROM mcr.microsoft.com/azure-cli:2.50.0

# Collect ARG from cli or use default
ARG TERRAFORM_VERSION=1.5.2
ARG KUBECTL_VERSION=1.26.4

# Install core packages
RUN apk add --no-cache \
        unzip \
        wget \
        ca-certificates \
        curl \
        git

WORKDIR /root

# Azure CLI is finicky about the local python environment
ENV PYTHONNOUSERSITE=1

# Install Terraform
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
        && unzip terraform_*_linux_amd64.zip \
        && mv terraform /usr/local/bin/ \
        && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Install kubectl
RUN curl -LO https://dl.k8s.io/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl \
        && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
        && rm kubectl

# Install kubens/kubectx
RUN git clone https://github.com/ahmetb/kubectx /opt/kubectx \
    && chmod +x /opt/kubectx/kubens /opt/kubectx/kubectx \
    && ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx \
    && ln -s /opt/kubectx/kubens /usr/local/bin/kubens
