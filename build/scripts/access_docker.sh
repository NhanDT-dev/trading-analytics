#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Print functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Container management functions
manage_containers() {
    while true; do
        clear
        echo -e "${CYAN}=== Docker Containers ===${NC}"
        echo "1. List all containers"
        echo "2. View container logs"
        echo "3. Execute into container"
        echo "4. Inspect container"
        echo "5. Restart container"
        echo "6. Stop container"
        echo "7. Remove container"
        echo "8. Remove all stopped containers"
        echo "q. Back to main menu"
        
        read -p "Select an option: " choice
        
        case $choice in
            1)
                echo -e "\n${CYAN}=== Running Containers ===${NC}"
                docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
                read -p "Press Enter to continue..."
                ;;
            2)
                containers=($(docker ps -a --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container to view logs:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        docker logs -f "$container"
                        break
                    fi
                done
                read -p "Press Enter to continue..."
                ;;
            3)
                containers=($(docker ps --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container to execute into:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        docker exec -it "$container" /bin/bash
                        break
                    fi
                done
                ;;
            4)
                containers=($(docker ps -a --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container to inspect:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        docker inspect "$container" | less
                        break
                    fi
                done
                ;;
            5)
                containers=($(docker ps -a --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container to restart:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        docker restart "$container"
                        print_success "Container $container restarted"
                        break
                    fi
                done
                ;;
            6)
                containers=($(docker ps --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container to stop:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        docker stop "$container"
                        print_success "Container $container stopped"
                        break
                    fi
                done
                ;;
            7)
                containers=($(docker ps -a --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container to remove:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        docker rm -f "$container"
                        print_success "Container $container removed"
                        break
                    fi
                done
                ;;
            8)
                read -p "Are you sure you want to remove all stopped containers? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    docker container prune -f
                    print_success "All stopped containers removed"
                fi
                ;;
            q|Q)
                return
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

# Image management functions
manage_images() {
    while true; do
        clear
        echo -e "${CYAN}=== Docker Images ===${NC}"
        echo "1. List all images"
        echo "2. Remove image"
        echo "3. Remove all unused images"
        echo "q. Back to main menu"
        
        read -p "Select an option: " choice
        
        case $choice in
            1)
                echo -e "\n${CYAN}=== Images ===${NC}"
                docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
                read -p "Press Enter to continue..."
                ;;
            2)
                images=($(docker images --format "{{.Repository}}:{{.Tag}}"))
                echo -e "\n${CYAN}Select an image to remove:${NC}"
                select image in "${images[@]}"; do
                    if [ -n "$image" ]; then
                        docker rmi -f "$image"
                        print_success "Image $image removed"
                        break
                    fi
                done
                ;;
            3)
                read -p "Are you sure you want to remove all unused images? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    docker image prune -af
                    print_success "All unused images removed"
                fi
                ;;
            q|Q)
                return
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

# Volume management functions
manage_volumes() {
    while true; do
        clear
        echo -e "${CYAN}=== Docker Volumes ===${NC}"
        echo "1. List all volumes"
        echo "2. Inspect volume"
        echo "3. Navigate to volume location"
        echo "4. Remove volume"
        echo "5. Remove all unused volumes"
        echo "q. Back to main menu"
        
        read -p "Select an option: " choice
        
        case $choice in
            1)
                echo -e "\n${CYAN}=== Volumes ===${NC}"
                docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"
                read -p "Press Enter to continue..."
                ;;
            2)
                volumes=($(docker volume ls --format "{{.Name}}"))
                echo -e "\n${CYAN}Select a volume to inspect:${NC}"
                select volume in "${volumes[@]}"; do
                    if [ -n "$volume" ]; then
                        docker volume inspect "$volume" | less
                        break
                    fi
                done
                ;;
            3)
                volumes=($(docker volume ls --format "{{.Name}}"))
                echo -e "\n${CYAN}Select a volume to navigate to:${NC}"
                select volume in "${volumes[@]}"; do
                    if [ -n "$volume" ]; then
                        location=$(docker volume inspect -f '{{.Mountpoint}}' "$volume")
                        print_success "Navigating to $location"
                        cd "$location"
                        exec $SHELL
                        break
                    fi
                done
                ;;
            4)
                volumes=($(docker volume ls --format "{{.Name}}"))
                echo -e "\n${CYAN}Select a volume to remove:${NC}"
                select volume in "${volumes[@]}"; do
                    if [ -n "$volume" ]; then
                        docker volume rm "$volume"
                        print_success "Volume $volume removed"
                        break
                    fi
                done
                ;;
            5)
                read -p "Are you sure you want to remove all unused volumes? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    docker volume prune -f
                    print_success "All unused volumes removed"
                fi
                ;;
            q|Q)
                return
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

# Network management functions
manage_networks() {
    while true; do
        clear
        echo -e "${CYAN}=== Docker Networks ===${NC}"
        echo "1. List all networks"
        echo "2. Connect container to network"
        echo "3. Disconnect container from network"
        echo "4. Remove network"
        echo "5. Remove all unused networks"
        echo "q. Back to main menu"
        
        read -p "Select an option: " choice
        
        case $choice in
            1)
                echo -e "\n${CYAN}=== Networks ===${NC}"
                docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"
                read -p "Press Enter to continue..."
                ;;
            2)
                containers=($(docker ps --format "{{.Names}}"))
                networks=($(docker network ls --format "{{.Name}}"))
                echo -e "\n${CYAN}Select a container:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        echo -e "\n${CYAN}Select a network:${NC}"
                        select network in "${networks[@]}"; do
                            if [ -n "$network" ]; then
                                docker network connect "$network" "$container"
                                print_success "Container $container connected to network $network"
                                break
                            fi
                        done
                        break
                    fi
                done
                ;;
            3)
                containers=($(docker ps --format "{{.Names}}"))
                echo -e "\n${CYAN}Select a container:${NC}"
                select container in "${containers[@]}"; do
                    if [ -n "$container" ]; then
                        networks=($(docker network inspect -f '{{range $net, $conf := .Containers}}{{$net}} {{end}}' "$container"))
                        echo -e "\n${CYAN}Select a network to disconnect from:${NC}"
                        select network in "${networks[@]}"; do
                            if [ -n "$network" ]; then
                                docker network disconnect "$network" "$container"
                                print_success "Container $container disconnected from network $network"
                                break
                            fi
                        done
                        break
                    fi
                done
                ;;
            4)
                networks=($(docker network ls --format "{{.Name}}"))
                echo -e "\n${CYAN}Select a network to remove:${NC}"
                select network in "${networks[@]}"; do
                    if [ -n "$network" ]; then
                        docker network rm "$network"
                        print_success "Network $network removed"
                        break
                    fi
                done
                ;;
            5)
                read -p "Are you sure you want to remove all unused networks? (y/n) " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    docker network prune -f
                    print_success "All unused networks removed"
                fi
                ;;
            q|Q)
                return
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
    done
}

# Main menu
while true; do
    clear
    echo -e "${CYAN}=== Docker Management Tool ===${NC}"
    echo "1. Manage Containers"
    echo "2. Manage Images"
    echo "3. Manage Volumes"
    echo "4. Manage Networks"
    echo "q. Exit"
    
    read -p "Select an option: " choice
    
    case $choice in
        1)
            manage_containers
            ;;
        2)
            manage_images
            ;;
        3)
            manage_volumes
            ;;
        4)
            manage_networks
            ;;
        q|Q)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid option"
            ;;
    esac
done
