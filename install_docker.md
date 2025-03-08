# Install Docker on Ubuntu

## Steps:

### 1. Update system packages:
```sh
sudo apt update && sudo apt full-upgrade
```

### 2. Add Docker repository and GPG key:
```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```sh
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

### 3. Install Docker and Docker Compose:
```sh
sudo apt update
```

```sh
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 4. Add user to Docker group (optional, but recommended for full access):
```sh
sudo usermod -aG docker root
```

### 5. Verification:
#### Check Docker version:
```sh
docker version
```

#### Check Docker Compose version:
```sh
docker compose version
```

thanks