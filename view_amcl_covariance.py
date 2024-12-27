import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped

import numpy as np
import matplotlib.pyplot as plt


class AMCLPoseCovarianceLogger(Node):
    def __init__(self):
        super().__init__('amcl_pose_covariance_logger')
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/amcl_pose',
            self.amcl_pose_callback,
            10
        )

        # matplotlib 인터랙티브 모드 설정
        plt.ion()

        # 초기 히트맵 설정
        self.fig, self.ax = plt.subplots()
        self.cov_matrix = np.zeros((6, 6))

        # 초기 히트맵 표시 (색상 범위는 임의로 0~1로 설정)
        self.heatmap = self.ax.imshow(
            self.cov_matrix,
            cmap='hot',
            interpolation='nearest',
            vmin=0,
            vmax=1
        )
        self.fig.colorbar(self.heatmap, ax=self.ax)
        self.ax.set_title('AMCL Pose Covariance Heatmap')
        plt.show(block=False)  # non-blocking

    def amcl_pose_callback(self, msg):
        # PoseWithCovarianceStamped 메시지의 covariance 정보를 6x6 행렬로 변환
        self.cov_matrix = np.array(msg.pose.covariance).reshape(6, 6)

        # 히트맵 데이터 갱신
        self.heatmap.set_data(self.cov_matrix)

        # 데이터 범위에 맞춰 컬러 스케일 재설정
        self.heatmap.set_clim(vmin=self.cov_matrix.min(), vmax=self.cov_matrix.max())

        # 그래프 다시 그려주기
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def main(args=None):
    rclpy.init(args=args)
    node = AMCLPoseCovarianceLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
