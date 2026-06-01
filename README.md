# system_hss

URDF modelleme, Gazebo simülasyonu, `ros2_control` ve RViz görselleştirmesini bir araya getiren bir ROS 2 paketi.

## İçerik

| Klasör | Açıklama |
|---|---|
| `urdf/` | Robotun URDF / Xacro tanımları |
| `meshes/` | 3B model dosyaları (görsel ve collision mesh'leri) |
| `gazebo/` | Gazebo simülasyon dünyaları ve eklenti yapılandırmaları |
| `ros2_control/` | `ros2_control` denetleyici yapılandırmaları |
| `rviz/` | Hazır RViz görselleştirme yapılandırmaları |
| `config/` | Ek parametre dosyaları |
| `launch/` | ROS 2 launch dosyaları |

## Gereksinimler

- ROS 2 (Humble veya üzeri önerilir)
- Gazebo (`gazebo_ros` / `ros_gz_bridge`)
- Aşağıdaki paketler:
  - `robot_state_publisher`
  - `joint_state_publisher`
  - `xacro`
  - `ros2_control` ve ilgili denetleyiciler

Ubuntu üzerinde temel bağımlılıkları kurmak için:

```bash
sudo apt install ros-$ROS_DISTRO-robot-state-publisher \
                 ros-$ROS_DISTRO-joint-state-publisher \
                 ros-$ROS_DISTRO-xacro \
                 ros-$ROS_DISTRO-gazebo-ros-pkgs \
                 ros-$ROS_DISTRO-ros-gz-bridge \
                 ros-$ROS_DISTRO-ros2-control \
                 ros-$ROS_DISTRO-ros2-controllers
```

## Kurulum

Paketi kendi ROS 2 workspace'inize klonlayın ve derleyin:

```bash
cd ~/ros2_ws/src
git clone https://github.com/Qaroom/system_hss.git
cd ~/ros2_ws
colcon build --packages-select system_hss
source install/setup.bash
```

## Kullanım

Paket içindeki launch dosyalarından birini çalıştırın:

```bash
ros2 launch system_hss last_system_hss.launch.py
```

`launch/` klasöründeki dosya isimlerine göre uygun komutu seçin (örneğin Gazebo simülasyonu, RViz görselleştirme veya `ros2_control` ile kontrol başlatma).

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında yayımlanmıştır.  
Copyright (c) 2026 Akram Al Qasemi
