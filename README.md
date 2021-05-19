# OpenCV-Object-Tracking
**Chú ý: ** nên cài opencv bằng lệnh `pip install opencv-contrib-python`

Trong bài trước chúng ta đã tìm hiểu về `centroid tracking algorithm`. Nó hoạt động khá tốt, tuy nhiên nó cần chạy `object detection` cho mỗi khung hình. Điều này sẽ làm tăng khối lượng tính toán hơn.

Chúng ta mong muốn chỉ thực hiện object detection một lần, sau đó sẽ thực hiện tracking. Phương pháp này sẽ hiệu quả và nhanh hơn. 

OpenCv cung cấp cho chúng ta 8 object tracking algorithms:
* **BOOOSTING tracker**: sử dụng các thuật toán AdaBoost (tương tự như Haar cascades sử dụng cho face detector). Tracker này chậm và không hoạt động tốt
* **MIL tracker**: độ chính xác cao hơn BOOSTIG nhưng nói chung vẫn kém
* **KCF tracker**: Kernelized Correlation Filters. Nhanh hơn BOOSTING và MILL. KCF và MIL đều không xử lý hoàn toàn được occlusion (hiện tượng các vật thể quá gần nhau dường như nối thành một, điều này gây khó khăn cho việc tracking)
* **CSRT tracker:** Discrimitive Correlation Filter (with Channel and Spatial Reliability). CSRT chính xác hơn KCF nhưng chậm hơn một chút
* **MedianFlow tracker:** hoạt đồng tương đối tốt, tuy nhiên nếu có nhiều sự thay đổi trong hành động như di chuyển nhanh của vật thể hoặc vật thể thay đổi nhanh chóng về hình dạng thì model có thể thất bại trong việc tracking
* **TLD tracker:** rất hay bị False-Positive (dương tính giả). Không nên sử dụng caí này.
* **MOSSE tracker:** rất nhanh, tuy nhiên độ chính xác không tốt như KCF và CSRT
* **GOTURN tracker:** dựa trên deep learning, cần nhiều files để chạy, khó sử dụng.

**Lời khuyên:**
- Sử dụng CSRT khi cần độ chính xác cao hơn và chịu giảm FPS một chút
- Dùng KCF nếu cần FPS cao nhưng độ chính xác có thể thấp hơn
- Dùng MOSSE khi cần tốc độ

# Tài liệu tham khảo
https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/

https://learnopencv.com/object-tracking-using-opencv-cpp-python/ 

