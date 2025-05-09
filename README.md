# AI_personal_project
1. Mục tiêu
Mục tiêu của chương trình là xây dựng một hệ thống giải bài toán 8-Puzzle bằng cách áp dụng nhiều nhóm thuật toán khác nhau trong lĩnh vực Trí Tuệ Nhân Tạo. Việc này nhằm so sánh hiệu quả giữa các thuật toán, hiểu rõ đặc điểm, ưu nhược điểm của từng phương pháp trong việc giải quyết bài toán tìm kiếm, từ đó nâng cao khả năng chọn lựa giải pháp phù hợp cho các vấn đề tương tự trong thực tế.

2. Nội dung
Chương trình được tổ chức thành nhiều nhóm thuật toán dựa theo phân loại trong AI:

  1.Uniformed Search: BFS, DFS, UCS, IDDFS

  2.Informed Search: Greedy, A*, IDA*, Genetic Algorithm (GA), Beam Search

  3.Local Search: Simple Hill Climbing, Steepest Hill Climbing, Stochastic Hill Climbing, Simulated Annealing (SA)

  4.Complex Environments: Nondeterministic search, No observation search, Partially observable search

  5.Constraint Satisfaction Problems (CSPs): Backtracking, Min-conflict, Backtracking with Forward Checking

  6.Reinforcement Learning: Q-Learning

2.1. Các thuật toán tìm kiếm có thông tin (Informed Search)
  a. Các thành phần chính của bài toán tìm kiếm
Một bài toán tìm kiếm bao gồm các thành phần chính:

  + Trạng thái ban đầu (Initial state): vị trí xuất phát của các ô trong 8-puzzle.
  + Tập hành động (Actions): các di chuyển hợp lệ của ô trống (trái, phải, lên, xuống).
  + Hàm chuyển trạng thái (Transition model): mô tả kết quả sau khi thực hiện hành động.
  + Mục tiêu (Goal state): trạng thái cuối cần đạt (ví dụ: các ô ở đúng vị trí theo thứ tự).
  + Hàm đánh giá (Heuristic function): dùng để ước lượng chi phí còn lại từ trạng thái hiện tại đến trạng thái mục tiêu (chỉ có trong các thuật toán có thông tin).
  + Solution: là chuỗi các hành động từ trạng thái ban đầu đến trạng thái mục tiêu sao cho tối ưu theo tiêu chí thời gian hoặc chi phí.

b. Nhận xét về hiệu suất của thuật toán khi áp dụng lên 8-Puzzle và hình ảnh (gif) minh họa.
![bfs](https://github.com/user-attachments/assets/ea3a408d-5e41-41c3-9bff-a147eb8d53ea)

IDA*
![IDA](https://github.com/user-attachments/assets/f540281c-17c7-4aa0-bf0d-f1182f02ff3c)
Cách hoạt động:

    Khởi tạo:
    Tính f(start) = g(start) + h(start), trong đó:
    g(n): chi phí thực từ gốc đến n (số bước).
    h(n): heuristic (ví dụ: khoảng cách Manhattan).
    Đặt ngưỡng ban đầu (threshold) bằng f(start).
    Lặp lại cho đến khi tìm được lời giải:
    Gọi hàm tìm kiếm theo chiều sâu có giới hạn depth_limited_search(threshold).
    Trong mỗi lần tìm kiếm:
    Duyệt theo chiều sâu, chỉ mở rộng các trạng thái có f(n) ≤ threshold.
    Nếu trạng thái đích được tìm thấy → trả về lời giải.
    Nếu tất cả trạng thái vượt quá threshold → lưu lại giá trị f(n) nhỏ nhất vượt ngưỡng (min_threshold).
    Cập nhật threshold = min_threshold và lặp lại.
    Kết thúc khi tìm thấy lời giải hoặc không còn trạng thái để mở rộng.

Ưu điểm:
Bộ nhớ thấp hơn A* vì dùng DFS chứ không lưu toàn bộ hàng đợi.
Vẫn đảm bảo tìm được lời giải tối ưu nếu heuristic chấp nhận được.

Nhược điểm:
Tốn thời gian hơn A* do phải duyệt lại nhiều trạng thái ở các vòng lặp sau.
Nếu không tối ưu heuristic, số lần lặp có thể tăng cao.

  - Beam Search: Tương tự BFS nhưng chỉ giữ lại số lượng trạng thái tốt nhất giới hạn (beam width) tại mỗi mức.
  + Beam Search: có thể nhanh nếu chọn được kích thước beam hợp lý nhưng không đảm bảo tìm được lời giải tối ưu.
    ![beam](https://github.com/user-attachments/assets/9e31a041-df47-4501-890e-de4192f9d398)
  - Genetic Algorithm (GA): Sử dụng cơ chế chọn lọc tự nhiên (lai ghép, đột biến) để tiến hóa lời giải qua nhiều thế hệ.
  + Genetic Algorithm: không luôn tìm ra lời giải tối ưu, phụ thuộc nhiều vào cách biểu diễn cá thể và hàm fitness; tuy nhiên có thể hiệu quả trong không gian tìm kiếm lớn hoặc không xác định.

Greedy Search
    ![Gready](https://github.com/user-attachments/assets/2edf4f5c-219b-47b3-af8f-671335c90f0a)
Cách hoạt động:

    Khởi tạo:
    Đưa trạng thái ban đầu vào hàng đợi ưu tiên (priority queue).
    Tính giá trị heuristic (tổng khoảng cách Manhattan).
    Lặp lại cho đến khi hàng đợi rỗng hoặc tìm thấy trạng thái đích:
    Lấy trạng thái có giá trị heuristic nhỏ nhất ra khỏi hàng đợi.
    Nếu trạng thái là đích → trả về lời giải.
    Sinh các trạng thái con từ các hành động hợp lệ (di chuyển ô trống).
    Với mỗi trạng thái con, tính heuristic và đưa vào hàng đợi.
    Không sử dụng chi phí từ gốc đến trạng thái hiện tại (g(n)), chỉ dùng heuristic h(n).

Ưu điểm:
Nhanh, ít bộ nhớ.
Dễ cài đặt.

Nhược điểm:
Không đảm bảo tìm được lời giải tối ưu.
Dễ bị lạc vào hướng sai do chỉ nhìn trước một bước.

A Search 
    ![A](https://github.com/user-attachments/assets/4fe45389-afc1-481b-b7b6-d45018ff7274)
Cách hoạt động:

    Khởi tạo:
    Đưa trạng thái ban đầu vào hàng đợi ưu tiên (priority queue).
    Tính giá trị f(n) = g(n) + h(n) cho mỗi trạng thái:
    g(n): chi phí từ trạng thái ban đầu đến trạng thái hiện tại (thường là số bước đi).
    h(n): heuristic – ước lượng chi phí còn lại để đến trạng thái đích (khoảng cách Manhattan).
    Lặp lại cho đến khi hàng đợi rỗng hoặc tìm thấy trạng thái đích:
    Lấy trạng thái có giá trị f(n) nhỏ nhất ra khỏi hàng đợi.
    Nếu là trạng thái đích → trả về đường đi.
    Sinh các trạng thái con từ các hành động hợp lệ.
    Với mỗi trạng thái con:
    Tính g(n), h(n), và f(n).
    Nếu chưa được thăm hoặc tìm được đường đi tốt hơn → đưa vào hàng đợi.

Ưu điểm:
Tìm được lời giải ngắn nhất nếu heuristic tốt.
Hiệu quả hơn Uniformed Search như UCS hay BFS trong nhiều trường hợp.

Nhược điểm:
Tốn bộ nhớ nếu không gian trạng thái lớn (do lưu toàn bộ trạng thái mở và đóng).
Hiệu suất phụ thuộc mạnh vào độ chính xác của heuristic.
