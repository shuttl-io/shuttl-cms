from shuttl.Models.FileTree.TreeNodeObject import TreeNodeObject
from shuttl.Models.Website import Website
from shuttl.Models.Queue import Queue, QueueIsEmptyException
from shuttl.tests import testbase

class QueueTestCase(testbase.BaseTest):

    def test_treeNodes(self):
        test1 = TreeNodeObject.Create(name="test1")
        test2 = TreeNodeObject.Create(name="test2")
        test3 = TreeNodeObject.Create(name="test3")
        test4 = TreeNodeObject.Create(name="test4")

        Queue.Push(fileObject=test1)
        Queue.Push(fileObject=test2)
        Queue.Push(fileObject=test3)
        Queue.Push(fileObject=test4)

        self.assertFalse(Queue.Empty())
        self.assertEquals(Queue.query.filter(Queue.recoverable==True).count(), 4)

        obj = Queue.Pop()
        self.assertFalse(Queue.Empty())
        self.assertEquals(Queue.query.filter(Queue.recoverable==True).count(), 3)
        self.assertEqual(obj, test1)

        obj = Queue.Pop()
        self.assertFalse(Queue.Empty())
        self.assertEquals(Queue.query.filter(Queue.recoverable==True).count(), 2)
        self.assertEqual(obj, test2)

        obj = Queue.Pop()
        self.assertFalse(Queue.Empty())
        self.assertEquals(Queue.query.filter(Queue.recoverable==True).count(), 1)
        self.assertEqual(obj, test3)

        obj = Queue.Pop()
        self.assertTrue(Queue.Empty())
        self.assertEquals(Queue.query.filter(Queue.recoverable==True).count(), 0)
        self.assertEqual(obj, test4)

        self.assertRaises(QueueIsEmptyException, Queue.Pop)
        pass
