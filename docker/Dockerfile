# Dockerfile for FreeBSD Custom OS Builder
# Provides a containerized build environment

FROM freebsd:14.0

# Install dependencies
RUN pkg update && pkg install -y \
    git \
    python3 \
    py39-pip \
    gmake \
    && pkg clean -y

# Create workspace
WORKDIR /workspace

# Copy builder scripts
COPY . /workspace/

# Set environment
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["/bin/sh"]
