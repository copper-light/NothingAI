class Trainer(object):

    def __init__(self, name, model, dataset, epochs, learning_rate, batch_size):
        self.status = 'created'
        self.name = name
        self.model = model
        self.dataset = dataset
        self.epochs = epochs
        self.current_epoch = 0
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.accuracy = 0
        self.loss = 0

    def run(self):
        return True

    def get_status(self):
        return self.status

    # def callback_function(self, func):
    #     self.
    #     func()

